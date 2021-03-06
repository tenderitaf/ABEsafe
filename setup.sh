#!/bin/bash

if [[ `uname` == 'Linux' ]] && $(hash apt-get 2>/dev/null); then
	sudo apt-get update
	sudo apt-get install -y wget git python python2.7-dev python-pip
	sudo apt-get install -y dpkg-dev build-essential libwebkitgtk-dev libgtk2.0-dev
	sudo apt-get install -y libjpeg-dev libtiff-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libnotify-dev
	sudo apt-get install -y freeglut3 freeglut3-dev
	sudo apt-get install -y libgmp3-dev M4 flex bison
	wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
	tar xf pbc-0.5.14.tar.gz
	cd pbc-0.5.14
	./configure
	make && sudo make install
	cd ..
	rm -rf pbc-0.5.14
	rm pbc-0.5.14.tar.gz
	sudo pip install --upgrade pip
	sudo pip install --upgrade setuptools
	sudo pip install --upgrade --trusted-host wxpython.org --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix
	
elif [[ `uname` == 'Darwin' ]]; then
	if ! [ $(hash brew 2>/dev/null) ]; then
		/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	fi
	brew update
	brew install git
	brew install glib gmp pbc
	brew install python
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install --upgrade --trusted-host wxpython.org --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix
else
	echo "It seems your system is not Mac OS X nor Debian Linux distribution, and is currently unsupported."
	exit 1
fi
