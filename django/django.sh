#!/bin/bash

sudo apt install python3-pip

export https_proxy=http://192.168.15.254:3128
sudo -E pip3 install django
sudo -E apt install libmysqlclient-dev 		# set system-proxy to NONE
sudo -E pip3 install mysqlclient

echo 'alias python="/usr/bin/python3"' > ~/.bash_aliases

