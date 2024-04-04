import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

GENDER = "male"
WEIGHT_KG = '64'
HEIGHT_CM = '175'
AGE = '18'

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

nutri_endpoint = os.environ["N_END"]
sheet_endpoint = os.environ["S_END"]
basic = HTTPBasicAuth(os.environ["NAME"], os.environ["PASS"])
did = input('tell me what you did: ')


headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

parameters = {
    "query": did,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

response = requests.post(nutri_endpoint, headers=headers, json=parameters)
response.raise_for_status()
data = response.json()

for i in range(len(data['exercises'])):
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            'exercise': data['exercises'][i]['name'],
            'duration': data['exercises'][i]['duration_min'],
            'calories': data['exercises'][i]['nf_calories']
        }
    }
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=basic)

    print(sheet_response.text)