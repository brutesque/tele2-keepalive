#!/usr/bin/env bash

set -e

sudo apt update
sudo apt install --yes git python-pip

sudo rm -Rf /tmp/tele2-keepalive
sudo git clone https://github.com/brutesque/tele2-keepalive /tmp/tele2-keepalive

sudo pip install -r /tmp/tele2-keepalive/requirements.txt

sudo cp /tmp/tele2-keepalive/tele2-keepalive.py /opt/
sudo cp /tmp/tele2-keepalive.service /lib/systemd/system/

sudo chmod 644 /lib/systemd/system/tele2-keepalive.service

sudo systemctl daemon-reload
sudo systemctl enable tele2-keepalive.service
