@echo off

:: Copy the icon to the temp folder
COPY RES\icon.ico %TEMP%\tic-tac-toe-icon.ico

:: Run 'pythonw --version' and put it into variable PYTHON_VERSION
FOR /F "tokens=* USEBACKQ" %%F IN (`pythonw --version`) DO (
SET PYTHON_VERSION=%%F
)

:: Check if Python 3 is installed
IF "%PYTHON_VERSION:~0,8%" == "Python 2" (
	:: If Python 2 is installed, show the message
	ECHO Your Python version is %PYTHON_VERSION%. You need to install Python 3 and set its path first.
	mshta javascript:alert^("Your Python version is %PYTHON_VERSION%. \nYou need to install Python 3 and set its path first."^);close^(^);
	start "" http://www.python.org/downloads/
	exit /b
)
IF NOT "%PYTHON_VERSION:~0,8%" == "Python 3" (
	:: If Python 3 is not installed, show the message
	ECHO You need to install Python 3 first.
	mshta javascript:alert^("You need to install Python 3 first."^);close^(^);
	start "" http://www.python.org/downloads/
	exit /b
)

:: Run the GUI python script
start "" pythonw ttt_client_gui.py