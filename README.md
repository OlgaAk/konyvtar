oracle vm free tier<br />
domain name free from https://www.duckdns.org/domains

usefull commands:
change env to test
export APP_ENV=test
flask run -h localhost -p 3001 --debug  
source venv/bin/activate  
pip install -r requirements.txt
chmod +x /home/ubuntu/webapp/scheduler.py
sudo systemctl daemon-reload
sudo systemctl enable webapp-scheduler
sudo systemctl start webapp-scheduler
sudo systemctl status webapp-scheduler
journalctl -u webapp-scheduler -f

sqlite3 app.db
.tables
