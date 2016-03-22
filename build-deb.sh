#!/bin/bash

VERSION='1.0'
PACKAGE_REVISION='1'
# Make a temperary directory for the debian package
mkdir tic-tac-toe-online_${VERSION}-${PACKAGE_REVISION}
chmod 0755 tic-tac-toe-online_${VERSION}-${PACKAGE_REVISION}
cd tic-tac-toe-online_${VERSION}-${PACKAGE_REVISION}

# Create the DEBIAN/control file
mkdir DEBIAN
cat >> DEBIAN/control << EOM
Package: tic-tac-toe-online
Version: ${VERSION}-${PACKAGE_REVISION}
Section: games 
Installed-Size: 226
Maintainer: Charlie Chen <Charlie@CharmySoft.com>
Homepage: http://www.CharmySoft.com/app/ttt-python.htm
Priority: optional
Architecture: all
Depends: python3
Description: Tic-Tac-Toe Online
 Simple yet fun noughts and crosses game online

EOM

# Create 'usr' folder
mkdir usr
# Create 'usr/bin/tic-tac-toe-online' script
mkdir usr/bin
cat >> usr/bin/tic-tac-toe-online << EOM
#!/bin/bash
/usr/share/tic-tac-toe-online/ttt_client_gui.py
EOM
# Add execution permission
chmod 0755 usr/bin/tic-tac-toe-online
# Create 'usr/share' folder
mkdir usr/share
# Create a menu entry
mkdir usr/share/applications
cat >> usr/share/applications/tic-toc-toe-online.desktop << EOM
[Desktop Entry]
Name=Tic-Tac-Toe Online
Version=${VERSION}
Exec=tic-tac-toe-online
Comment=Simple yet fun noughts and crosses game online
Icon=/usr/share/pixmaps/tic-tac-toe-online.png
Type=Application
Terminal=false
StartupNotify=true
Categories=Games;
EOM
# Add execution permission
chmod 0644 usr/share/applications/tic-toc-toe-online.desktop
# Copy the application icon
mkdir usr/share/pixmaps
cp ../icons/icon.png usr/share/pixmaps/tic-tac-toe-online.png
# Copy all the required files to 'usr/share/tic-tac-toe-online'
mkdir usr/share/tic-tac-toe-online
cp ../ttt_client.py usr/share/tic-tac-toe-online
cp ../ttt_client_gui.py usr/share/tic-tac-toe-online
cp ../res -r usr/share/tic-tac-toe-online/res
# Add execution permission
chmod 0755 usr/share/tic-tac-toe-online/ttt_client.py
chmod 0755 usr/share/tic-tac-toe-online/ttt_client_gui.py
# Build the debian package
cd .. 
chown -R root tic-tac-toe-online_${VERSION}-${PACKAGE_REVISION}
dpkg-deb --build tic-tac-toe-online_${VERSION}-${PACKAGE_REVISION}

# Remove the temperary folder
rm -r tic-tac-toe-online_${VERSION}-${PACKAGE_REVISION}
