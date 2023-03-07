import requests
import json
import datetime

from prefect import task, Flow
from prefect.schedules import IntervalSchedule

## extract
@task(cache_for=datetime.timedelta(days=1))
def get_price():
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=mxn")
    response_json = json.loads(r.text)
    return response_json

## transform
@task
def parse_data(raw):
    price = raw['dogecoin']['mxn']
    return price

## load
@task
def send_notificacion(parsed):
    token = "6191852587:AAEyCD59d37jirpOB2d0Zq-wMiTLBjCKjfo"
    url = f"https://api.telegram.org/bot{token}"
    if parsed < 1:
        params = {"chat_id": "5473415339", "text": "Compraaaa!!!!"}
        r = requests.get(url + "/sendMessage", params=params)
    elif parsed > 2.5:
        params = {"chat_id": "5473415339", "text": "vende!!!!"}
        r = requests.get(url + "/sendMessage", params=params)
schedule = IntervalSchedule(interval=datetime.timedelta(seconds=10))

with Flow("my etl flow",schedule) as f:
    raw = get_price()
    parsed = parse_data(raw)
    send_notificacion(parsed)

f.run()