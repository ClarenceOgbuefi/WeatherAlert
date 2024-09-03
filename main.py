import requests
import datetime as datetime
from twilio.rest import Client

# SMS Client Keys
ACCOUNT_SID = "Account SID from Twilio"
AUTH_TOKEN = "Authentication Token from Twilio"
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# Weather API Keys
API_KEY = "API Key from openweathermap API"
ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
NAME = "Clarence"


# Parameters for weather API
PARAMETERS = {
    "lat": 33.859760,
    "lon": -84.685432,
    "appid": API_KEY,
    "cnt": 4
}

# Weather API
response = requests.get(url=ENDPOINT, params=PARAMETERS)
response.raise_for_status()
weather_data = response.json()["list"]


# Creates message to be sent to user
def create_message():
    message = f"Hi {NAME}, here is the forecast for today:\n"
    for data in weather_data:
        hourly_forecast = weather_check(data)
        message = message + f"{hourly_forecast[0]}:{hourly_forecast[1]}\n"

    if rain_check():
        message = message + "You might want to carry an umbrella with you!"
    return message


# Checks if it will rain
def rain_check():
    will_it_rain = False
    for data in weather_data:
        if data["weather"][0]["id"] < 700:
            will_it_rain = True
    return will_it_rain


# Checks weather for the day
def weather_check(data):
    hour = datetime.datetime.strptime(data["dt_txt"], "%Y-%m-%d %H:%M:%S")
    hour = time_of_day(hour)
    forecast = data['weather'][0]['main']
    return hour, forecast


# Converts time to AM if needed
def time_of_day(time):
    if time.hour > 12:
        hour_of_day = f"{time.hour - 12}:00 PM"
    elif time.hour == 0:
        hour_of_day = "12:00 AM"
    else:
        hour_of_day = f"{time.hour}:00 AM"
    return hour_of_day


# SMS Client
text = CLIENT.messages.create(
    body=create_message(),
    from_="+18449812279",
    to="+14044555890",
)

print(text.status)


