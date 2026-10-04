# Одержати дані GDP per capita (current US$) для України за 1991–2019 роки. Зберегти одержані дані у форматі JSON та перетворити їх у формат CSV. Вивести на екран зміст отриманого JSON-файлу та створеного CSV-файлу.

import requests
from requests.exceptions import HTTPError, Timeout
import json
import csv

params = {
  "date": "1991:2019",
  "format": "json",
  "per_page": "100",
}

country = "ukr"
indicator = "NY.GDP.PCAP.CD"

API_WORLD_URL = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}/"

def get_data(url, params = {}):
  try:
    response = requests.get(url, params = params, timeout=8)
    response.raise_for_status()
    print("Data was successfully received")
    return response.json()
  except HTTPError as http_err:
    print(f"HTTP error: {http_err}")
    print(f"Error code: {response.status_code}")
  except Timeout:
    print("Request timed out")

def print_json(data, file_name = "new_data.json"):
  try:
    with open(file_name, "w", encoding="utf-8") as file:
      json.dump(data, file, ensure_ascii=False,  indent=4)
      print("Data was successfully saved in JSON format")
  except UnicodeEncodeError as e:
    print(f"Encoding error: {e}")

def check_value(val):
  if isinstance(val, (int, float)):
    return round(val, 4)

def print_csv(data, file_name = "new_data.csv"):
  if not data:
    print("No data to write to CSV")
    return
  
  try:
    with open(file_name, "w", newline="", encoding="utf-8-sig") as file:
      writer = csv.writer(file, delimiter=";")
      writer.writerow(["Country", "Indicator", "Year", "Value"])
      for item in data[1]:
        if item["value"] is not None:
          writer.writerow([item["country"]["value"], item["indicator"]["value"], item["date"], check_value(item["value"])])
  except TypeError as e:
    print(f"Type error: {e}")
  except PermissionError:
    print(f"Permission denied: Unable to write to {file_name}")
  except UnicodeEncodeError as e:
    print(f"Encoding error: {e}")

GDP = get_data(API_WORLD_URL, params)
print_json(GDP, "world-bank-data.json")
print_csv(GDP, "world-bank-data.csv")

def show_csv_data(file):
  try:
    with open(file, "r", encoding="utf-8") as file:
      reader = csv.reader(file)
      for line in reader:
        print(line)
  except FileNotFoundError:
    print(f"File {file} not found")

show_csv_data("world-bank-data.csv")