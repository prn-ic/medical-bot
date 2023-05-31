#!/bin/bash
pip3 install -r /home/zmqp/Документы/github/medical-bot/requirements.txt
sudo apt-get install libpq-dev python3-dev
pip3 install psycopg2
python3 /home/zmqp/Документы/github/medical-bot/main.py

