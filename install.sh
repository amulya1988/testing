#!/usr/bin/env bash

ps -ef|grep python|grep 9994

nohup uwsgi --http-socket 0.0.0.0:9994 --plugin python3 --wsgi-file application.py --master --processes 8 --threads 10 --stats 0.0.0.0:9192 --stats-http --buffer-size 20000 &

sudo su
cd /home/ec2-user/lnt/vdc_report_python
kill -9 $(sudo lsof nohup.out | awk '{print $2}' | grep -v 'PID')
kill -9 $(ps -ef|grep python|grep 9994|awk '{print $2}')
ps -ef|grep python|grep 9994
nohup /opt/uwsgi --http-socket 0.0.0.0:9994 --plugin python36 --wsgi-file application.py --master --processes 8 --threads 10 --stats 0.0.0.0:9192 --stats-http --buffer-size 20000 --http-buffer-size 20000 --http-connect-timeout 20000 --http-headers-timeout 20000
