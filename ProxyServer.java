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
		try {
			//args are host, remoteport, localport
			if ((args.length == 0) || (args.length % 3 != 0))
				throw new IllegalArgumentException("Wrong number of arguments");

			// Create the Server object
			Server s = new Server(null, 10); //10 is max connections

			int i = 0;
			while(i < args.length) {
				String host = args[i++];
				int remoteport = Integer.parseInt(args[i++]);
				int localport = Integer.parseInt(args[i++]);
				s.addService(new Proxy(host, remoteport), localport);
			}
		}
		catch (Exception e) {  // Print an error message if anything goes wrong.
			System.err.println(e);
			System.err.println("Usage: java ProxyServer <host> <remoteport> <localport> ...");
			System.exit(1);
		}
	}

  
}