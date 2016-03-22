#!/bin/bash

VERSION='1.0'
PACKAGE_REVISION='1'
# Make a temperary directory for the debian package
mkdir tttpy_${VERSION}-${PACKAGE_REVISION}
chmod 0755 tttpy_${VERSION}-${PACKAGE_REVISION}
cd tttpy_${VERSION}-${PACKAGE_REVISION}

# Create the DEBIAN/control file
mkdir DEBIAN
cat >> DEBIAN/control << EOM
Package: tttpy
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
# Create 'usr/bin/tttpy' script
mkdir usr/bin
cat >> usr/bin/tttpy << EOM
#!/bin/bash
cd /opt/charmysoft/tttpy/
./ttt_client_gui.py
EOM
# Add execution permission
chmod 0755 usr/bin/tttpy
# Create 'usr/share' folder
mkdir usr/share
# Create a menu entry
mkdir usr/share/applications
cat >> usr/share/applications/tttpy.desktop << EOM
[Desktop Entry]
Name=Tic-Tac-Toe Online
Version=${VERSION}
Exec=tttpy
Comment=Simple yet fun noughts and crosses game online
Icon=/opt/charmysoft/tttpy/res/icon.png
Type=Application
Terminal=false
StartupNotify=true
Categories=Games;
EOM
# Add execution permission
chmod 0644 usr/share/applications/tttpy.desktop
# Copy all the required files to 'opt/charmysoft/tttpy'
mkdir opt && mkdir opt/charmysoft && mkdir opt/charmysoft/tttpy
cp ../ttt_client.py opt/charmysoft/tttpy
cp ../ttt_client_gui.py opt/charmysoft/tttpy
cp ../res -r opt/charmysoft/tttpy/res
# Add execution permission
chmod 0755 opt/charmysoft/tttpy/ttt_client.py
chmod 0755 opt/charmysoft/tttpy/ttt_client_gui.py
# Build the debian package
cd .. 
chown -R root tttpy_${VERSION}-${PACKAGE_REVISION}
dpkg-deb --build tttpy_${VERSION}-${PACKAGE_REVISION}

# Remove the temperary folder
rm -r tttpy_${VERSION}-${PACKAGE_REVISION}
