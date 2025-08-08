from bs4 import BeautifulSoup
from dotenv import load_dotenv, dotenv_values
from datetime import date
import requests
import json
import smtplib
import sys
import os

load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')
NAME = os.getenv('NAME')
SMPT = os.getenv('SMPT')
PORT = os.getenv('PORT')

def send_message(email, message):
  server = smtplib.SMTP('SMTP', 'PORT')
  server.starttls()
  server.login(EMAIL, PASSWORD)
  server.sendmail(EMAIL, email, message)

def shoes(url, id, shoe_name):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  price_element = soup.find("div", {"id": id})
  if not price_element:
    print("Price element not found.")
    return

  try:
    shoe_price = int(price_element.get_text().strip().replace('$', ''))
  except ValueError:
    print("Could not parse price")
    return

  today = date.today()
  shoe_price_today = {
    'Shoe Name': shoe_name,
    'Shoe Price': shoe_price,
    'Today\'s Date': today.isoformat()
  }

  try:
    with open('data.json', 'r') as f:
      data = json.load(f)
  except (FileNotFoundError, json.JSONDecodeError):
    data = None

  if data is None or data['Shoe Price'] != shoe_price:
    if data:
      if shoe_price > data['Shoe Price']:
        message = f"Hey {NAME}! Moogbot here in your inbox to tell you that the price of the {shoe_name} has gone up! Now {shoe_price} as of {today}. I'll send you another email when it changes."
      else: 
        message = f"Hey {NAME}! Moogbot here in your inbox to tell you that the price of the {shoe_name} has gone down! Now {shoe_price} as of {today}. I'll send you another email when it changes."
      send_message(TO_EMAIL, message)
  
    with open('data.json', 'w') as f:
      json.dump(shoe_price_today, f)

shoes('https://www.nike.com/t/pegasus-41-mens-road-running-shoes-LMhfRGdO/FD2722-002', 'price-container', 'Nike Pegasus 41')
