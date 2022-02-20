#!/bin/bash

apt clean
apt update -y
apt install -y apache2
echo "This is my Webserver " > /var/www/html/index.html
service apache2 restart