import datetime
import configparser
import os
import sys

import requests
from bs4 import BeautifulSoup


config_file = 'cybrary_login.ini'
log_file = 'cybrary_login.log'

config = configparser.ConfigParser()
config.read(config_file)
USER = config["LoginInfo"].get("USER")
PASSWORD = config["LoginInfo"].get("PASSWORD")

s = requests.session()
login_data = dict(log=USER, pwd=PASSWORD)
s.post('https://www.cybrary.it/wp-login.php?', data=login_data)
r = s.get('https://www.cybrary.it')

try:
    [c for c in s.cookies.keys() if 'logged_in' in c][0]
except IndexError:
    print("Error: Invalid Username or Password!")
    sys.exit()

print('Logged in!')

soup = BeautifulSoup(r.content, 'lxml')
cybytes = soup.find('div', class_='cybytes')
cybytes_nr = cybytes.get_text().rstrip()

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M") + ' | Nr of Cybytes: ', cybytes_nr)

with open(log_file, "a") as f:
    f.write(now.strftime("%Y-%m-%d %H:%M"))
    f.write(str(' | Nr of Cybytes: ' + cybytes_nr + '\n'))
