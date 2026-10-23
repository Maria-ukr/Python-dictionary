import requests
from requests.exceptions import HTTPError, Timeout
import csv
import plotly.express as px
import pandas as pd

URL = "https://api.worldbank.org/v2/country/"

def get_counry_code(country):
  params = {"format": "json", "per_page": 300}
  try:
    response = requests.get(URL, params=params, timeout=8)
    response.raise_for_status()
    data = response.json()
    if len(data) > 1 and data[1]:
      for item in data[1]:
        if item["name"].lower() == country.lower():
          return item["id"].lower()
    print(f"Country: {country} wasn`t found")
  except (HTTPError, Timeout) as e:
    print(f"Error while searching the country: {e}")
    return None

def get_data(country):
  params = {
    "date": "1990:2025",
    "format": "json",
  }
  indicator = "SP.POP.TOTL"
  url = f"{URL}{country}/indicator/{indicator}/"
  file_name = f"demographic-data-{country.lower()}.csv"
  try:
    response = requests.get(url, params = params, timeout=8)
    response.raise_for_status()
    print(f"Data was successfully received for {country}")
    print_csv(response.json(), file_name)
    return file_name
  except HTTPError as http_err:
    print(f"HTTP error: {http_err} for country {country}")
    print(f"Error code: {response.status_code}")
  except Timeout:
    print(f"Request timed out for country {country}")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

def print_csv(data, file_name = "new_data.csv"):
  if not data or len(data) < 2 or not data[1]:
    print("No data to write to CSV")
    return
  
  try:
    with open(file_name, "w", newline="", encoding="utf-8-sig") as file:
      writer = csv.writer(file, delimiter=";")
      writer.writerow(["Year", "Million", "Country"])
      for item in data[1]:
        if item["value"] is not None:
          writer.writerow([item["date"], item["value"], item["country"]["value"]])
  except TypeError as e:
    print(f"Type error: {e}")
  except PermissionError:
    print(f"Permission denied: Unable to write to {file_name}")
  except UnicodeEncodeError as e:
    print(f"Encoding error: {e}")

while True:
  user_input = input("Enter counry in English for demographic comparison with Ukraine: ").strip()
  if user_input.lower() == "exit":
    exit()
  comparCountry = get_counry_code(user_input)
  if comparCountry:
    break
  else:
    print(f"Country: '{user_input}' wasn't found. Type right country.\n")

# TASK 4: Create pie
while True:
  input_year = input("Enter year for comparison: ")
  if input_year.isdigit():
    year_int = int(input_year)
    if 1990 <= year_int <= 2025:
      break
  print(f"'{input_year}' is wrong. Type year in range between 1990 - 2025.\n")

fileUkraine = get_data("ukr")
fileComparCountry = get_data(comparCountry)

if fileUkraine and fileComparCountry:
  df_fileUkraine = pd.read_csv(fileUkraine, sep=";")
  df_fileComparCountry = pd.read_csv(fileComparCountry, sep=";")

  df_combine = pd.concat([df_fileUkraine, df_fileComparCountry], ignore_index=True)
  df_combine["Year"] = pd.to_numeric(df_combine["Year"])
  df_filter = df_combine[df_combine["Year"] == year_int]

  fig = px.pie(
    df_filter,
    names="Country",
    values="Million",
    title=f"Population Comparison for {year_int}",
  )
  fig.update_traces(textinfo="percent+label", textfont_size=14)
  fig.update_layout(
    height=600,
    title_font_textcase="upper",
    title=dict(
      x=0.5,
      xanchor="center",
      font=dict(color="#1b975a", size=18, weight="bold"),
    ),
  )
  fig.show()

else:
  print("Can`t found countries")