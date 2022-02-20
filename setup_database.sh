#!/bin/bash

apt clean
apt update -y
apt install -y mysql-server mysql-client
service mysql restart