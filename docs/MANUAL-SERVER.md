Manual for Tic-Tac-Toe Server
========================
To start the server, run ttt_server.py with  

	ttt_server.py [port_number]

Where the argument *port_number* is a 16-bit unsigned integer port number used for the TCP/IP protocol addressing. You can also run the server script with no arguments, and you will then be asked to enter the and port number.  

![Server Error](./img/server-error.png?raw=true "Server Error")  
If the server fails to bind the port, you will see an error message as above. You can then choose to abort, change port number, or retry, as you wish. Usually this is due to port conflicts, or the port is reserved by the system.  

![Server Start](./img/server-start.png?raw=true "Server Start")  
When the server is successfully started, you will see some messages as above. And then the server will be able to accept clients.  

![Server Running](./img/server-running.png?raw=true "Server Running")  
You will be informed when clients are connected, when they get matched and start a game, when they disconnect, when some unexpected error happens, and when they finish their game, etc. Once the server gets started, it should be able to keep running without getting interrupted. Even when the clients' connection fails, or some unexpected messages are received from the client, the server can handle those exceptions gracefully and inform you of the exceptions.  

![Server Log](./img/server-log.png?raw=true "Server Log")  
All the information, warnings, and exceptions, will also be logged into the file *ttt_server.log*.  