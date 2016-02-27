<img src="http://raw.github.com/CharmySoft/tic-tac-toe-in-python/master/icons/icon.png" width="48"/>&nbsp;&nbsp;**Tic Tac Toe Online in Python**
========================
Details of this project can be found on the [Tic Tac Toe project page][2] under:  
[*http://www.CharmySoft.com/app/ttt-python.htm*][2]

Introduction
------------------------
[Tic Tac Toe Online in Python][2] is a socket-based Client-Server application in Python that allows multi-players to connect to the server and play Tic Tac Toe online with other players.  
This project is originally for my Python Assignment in Semester 6 Computer Systems Admin 2.


Manual
------------------------
To start the server, run the ttt_server.py with  

	ttt_server.py [port_number]

Where the parameter *port_number* is a 16-bit unsigned integer port number used for the TCP/IP protocol addressing.  
![Server](/screenshots/man-start-server.png?raw=true "Server")

To start the client, run the ttt_client.py with 

	ttt_client.py [server_address] [port_number]

Where the parameter *server_address* is a string that represents a IPv4 address for the server; *port_number* is the port number that will be used to connect to the server.  
![Client](/screenshots/man-start-client.png?raw=true "Client")

To start the game, there needs to be more than one players. Start another client with the same parameters to connect to the same running server, and the game will get started.


References
------------------------
Please see the file [docs/REFERENCES.md](docs/REFERENCES.md).


Licensing
------------------------
Please see the file named [LICENSE](LICENSE).


Author
------------------------
* Charlie Chen  
	founder of [CharmySoft][1]


Contact
------------------------
* CharmySoft: [*http://www.CharmySoft.com/*][1]  
* About: [*http://www.CharmySoft.com/about.htm*][3]  

[1]: http://www.CharmySoft.com/ "CharmySoft"
[2]: http://www.CharmySoft.com/app/ttt-python.htm "Tic Tac Toe Online in Python"
[3]: http://www.CharmySoft.com/about.htm "About CharmySoft"