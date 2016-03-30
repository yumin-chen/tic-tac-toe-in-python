Tic-Tac-Toe Server Manual
========================
<small>Please read the updated version at [The Server Manual](http://chenyumin.com/p/tic-tac-toe-server-manual) or [docs/MANUAL-SERVER.md](docs/MANUAL-SERVER.md).</small>

To set up the server, you can run the following shell commands.  
```bash
# Change this to your desired path
TTT_SERVER_SCRIPT_PATH="/ttt_server.py"

# Download the server script to your specified destination
sudo wget -O $TTT_SERVER_SCRIPT_PATH http://github.com/CharmySoft/tic-tac-toe-in-python/raw/master/ttt_server.py

# Download the upstart configuration script
sudo wget -O /etc/init/ttt-service.conf http://github.com/CharmySoft/tic-tac-toe-in-python/raw/master/ttt-service.conf

# Update the server script path on the downloaded upstart conf file
sudo sed -i 's|'/ttt_server.py'|'${TTT_SERVER_SCRIPT_PATH}'|' /etc/init/ttt-service.conf
```
After setting up the upstart configuration script, if you have installed [upstart](http://upstart.ubuntu.com/) on your server machine, the server script will automatically run on system start up. And respawn will start it back up if it is killed or exits non-zero (like an uncaught exception), so the server script can always keep running on your server.  

If you want to test the server script on your local machine, you can run [ttt_server.py](http://github.com/CharmySoft/tic-tac-toe-in-python/raw/master/ttt_server.py) with python3:  

	python3 ttt_server.py [port_number]

Where the argument *port_number* is a 16-bit unsigned integer port number used for the TCP/IP protocol addressing. You can also run the server script with no arguments, and you will then be asked to enter the and port number.  

![Server Error](./img/server-error.png?raw=true "Server Error")  
If the server fails to bind the port, you will see an error message as above. You can then choose to abort, change port number, or retry, as you wish. Usually this is due to port conflicts, or the port is reserved by the system.  

![Server Start](./img/server-start.png?raw=true "Server Start")  
When the server is successfully started, you will see some messages as above. And then the server will be able to accept clients.  

![Server Running](./img/server-running.png?raw=true "Server Running")  
You will be informed when clients are connected, when they get matched and start a game, when they disconnect, when some unexpected error happens, and when they finish their game, etc. Once the server gets started, it should be able to keep running without getting interrupted. Even when the clients' connection fails, or some unexpected messages are received from the client, the server can handle those exceptions gracefully and inform you of the exceptions.  

![Server Log](./img/server-log.png?raw=true "Server Log")  
All the information, warnings, and exceptions, will also be logged into the file *ttt_server.log*.  