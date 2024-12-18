import time
import datetime
import uuid
import hmac
import hashlib
import requests
import random


from celery import shared_task


API_KEY="쿨SMS API KEY"
SECRET="쿨SMS SECRET API KEY"
random_num = random.randint(1000, 9999)
URL="https://api.coolsms.co.kr/messages/v4/send"


def generate_random_4_digit_number():
    return random.randint(1000, 9999)

# 예제 실행

def unique_id():
    return str(uuid.uuid1().hex)

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

def get_signature(key='', msg=''):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

def get_headers():
    api_key=API_KEY
    api_secret_key=SECRET
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    return {
        'Authorization': 'HMAC-SHA256 ApiKey=' + api_key + ', Date=' + date + ', salt=' + salt + ', signature=' +
                         get_signature(api_secret_key, data),
        'Content-Type': 'application/json; charset=utf-8'
    }



@shared_task
def send_msm():
    msg = {"message":{"to":"폰번호","from":"폰번호","text":f"현재시간\n{datetime.datetime.now()}"}}    
    res = requests.post(URL, headers=get_headers(), json=msg)
    print(res.text)

@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True