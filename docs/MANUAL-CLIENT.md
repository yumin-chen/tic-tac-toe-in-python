Tic-Tac-Toe Client Manual
========================
<small>Please read the updated version at [http://chenyumin.com/p/tic-tac-toe-client-manual](http://chenyumin.com/p/tic-tac-toe-client-manual).</small>

These are the instructions to use the command-line based Tic-Tac-Toe Client program. For the GUI version, please read [here](../README.md).  

To start the client, run [ttt_client.py](http://github.com/CharmySoft/tic-tac-toe-in-python/raw/master/ttt_client.py) with Python 3:  

	python3 ttt_client.py [server_address] [port_number]

Where the argument *server_address* is a string that represents the server address; *port_number* is the port that the tic-tac-toe server is listening to. You can also run the client script with no arguments, and you will then be asked to enter the server address and port number.  

![Client Connect Error](./img/client-connect-error.png?raw=true "Client Connect Error")  
If the server is not running, or the provided server address and port number are incorrect and it fails to connect to the server, you will be asked to choose to abort, change address and port number, or retry.  

There is a Tic-Tac-Toe server script set up running on *s.CharmySoft.com* with port *8080*. You can test the client with this server if you are connected to the Internet:

	python3 ttt_client.py s.CharmySoft.com 8080

To test the client with the server running on your local machine, please read [MANUAL-SERVER.md](MANUAL-SERVER.md) and follow the instructions to start the server first.  

![Client Connect Success](./img/client-connect-success.png?raw=true "Client Connect Success")  
If the connection with the server is successfully established, you will see a welcome message as above. And you will be waiting for another player to join the game. However, if you are testing this with the server running on your local machine, you will have to start another client by yourself and connect to the server to get the game started.  

![Client Game](./img/client-game.png?raw=true "Client Game")  
Once the game is started, you can follow the instructions and enter the position number to make a move. If the position number you entered is, however, already taken or invalid, you will be asked to re-enter the position number.  

![Client Result](./img/client-result.png?raw=true "Client Result")  
Repeat until the game is finished and you shall get the result if you win or lose.