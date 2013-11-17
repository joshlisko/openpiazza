import java.util.Scanner;

/*
 * Copyright (c) 2000 David Flanagan.  All rights reserved.
 * This code is from the book Java Examples in a Nutshell, 2nd Edition.
 * It is provided AS-IS, WITHOUT ANY WARRANTY either expressed or implied.
 * You may study, use, and modify it for any non-commercial purpose.
 * You may distribute it non-commercially as long as you retain this notice.
 * For a commercial use license, or to purchase the book (recommended),
 * visit http://www.davidflanagan.com/javaexamples2.
 */

public class ProxyServer {

	
	public static void main(String[] args) {

		if(args.length == 0){
			System.out.println("Welcome to the proxy server. Type quit to exit."); 
			System.out.println("Start a proxy by entering in <host> <remoteport> <localport>");
			System.out.println("For example: ");
			System.out.println("www.reddit.com 80 3000");
			System.out.println("https://piazza.com 443 4414");
			System.out.println();
			System.out.println();
			
			Scanner kb = new Scanner(System.in);
			while(true){
				System.out.print("Start proxy: ");
				String line = kb.nextLine();
				if(line.toLowerCase().equals("quit"))
					System.exit(1);
				String[] proxyArgs = line.split(" ");
				startServer(proxyArgs);
			}
		}
		else{
				startServer(args);
			}

	}
	
	public static void startServer(String[] args){
		try{
			if(args.length %3 !=0)
				throw new IllegalArgumentException("Wrong number of arguments");
			
			Server s = new Server(null, 100); //100 is max connections
			int i = 0;
			while(i < args.length) {
				String host = args[i++];
				int remoteport = Integer.parseInt(args[i++]);
				int localport = Integer.parseInt(args[i++]);
				s.addService(new Proxy(host, remoteport), localport);
			}
		}
		catch (Exception e){
			System.err.println(e);
			System.err.println("Usage: java ProxyServer <host> <remoteport> <localport> ...");
			System.exit(1);
		}
	}
  
}