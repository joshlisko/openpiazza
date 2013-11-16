/*
 * Copyright (c) 2000 David Flanagan.  All rights reserved.
 * This code is from the book Java Examples in a Nutshell, 2nd Edition.
 * It is provided AS-IS, WITHOUT ANY WARRANTY either expressed or implied.
 * You may study, use, and modify it for any non-commercial purpose.
 * You may distribute it non-commercially as long as you retain this notice.
 * For a commercial use license, or to purchase the book (recommended),
 * visit http://www.davidflanagan.com/javaexamples2.
 */

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

/**
   * This is the class that implements the proxy service.  The serve() method
   * will be called when the client has connected.  At that point, it must
   * establish a connection to the server, and then transfer bytes back and
   * forth between client and server.  For symmetry, this class implements
   * two very similar threads as anonymous classes.  One thread copies bytes
   * from client to server, and the other copies them from server to client.
   * The thread that invoke the serve() method creates and starts these 
   * threads, then just sits and waits for them to exit.
   **/
public class Proxy implements Server.Service {
	String host;
	int port;
	
	//Remember the host and port
	public Proxy(String host, int port) {
		this.host = host;
		this.port = port;
	}
	
	//Invokes when client connects
	public void serve(InputStream in, OutputStream out) {
		final InputStream from_client = in;
		final OutputStream to_client = out;
		final InputStream from_server;
		final OutputStream to_server;
	
		//try to establish connection
		Socket server;
		try { 
			server = new Socket(host, port); 
			from_server = server.getInputStream();
			to_server = server.getOutputStream();
		}
		catch (Exception e) {
			PrintWriter pw = new PrintWriter(new OutputStreamWriter(out));
			pw.println("Proxy server could not connect to " + host + ":" + port);
			pw.flush();
			pw.close();
			try { 
				in.close(); 
			} 
			catch (IOException ex) {}
			return;
		}
	
		// Create an array to hold two Threads.  
		final Thread[] threads = new Thread[2];
	
		// Define and create a thread to transmit bytes from client to server
		Thread c2s = new Thread() {
			@SuppressWarnings("deprecation")
			public void run() {
				byte[] buffer = new byte[2048];
				int bytes_read;
				try {
					while((bytes_read = from_client.read(buffer)) != -1) {
						to_server.write(buffer, 0, bytes_read);
						to_server.flush();
					}
				}
				catch (IOException e) {}
	
				// if the client closed its stream to us, we close our stream
				threads[1].stop();
				try { 
					to_server.close(); 
				} 
				catch (IOException e) {}
			}
		};
	
		// Define and create a thread to copy bytes from server to client.
		Thread s2c = new Thread() {
			@SuppressWarnings("deprecation")
			public void run() {
				byte[] buffer = new byte[2048];
				int bytes_read;
				try {
					while((bytes_read = from_server.read(buffer)) != -1) {
						to_client.write(buffer, 0, bytes_read);
						to_client.flush();
					}
				}
				catch (IOException e) {}
	
				// if the server closed its stream to us, we close our stream
				threads[0].stop();
				try { 
					to_client.close(); 
				} 
				catch (IOException e) {}
			}
		};
	
		// Store the threads into the final threads[] array, 
		threads[0] = c2s; threads[1] = s2c;
	
		// start the threads
	  	c2s.start(); s2c.start();
	
	    try { 
	    	c2s.join(); s2c.join(); 
	    } 
	    catch (InterruptedException e) {}
	}
}
