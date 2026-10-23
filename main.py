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
  
fileUkraine = get_data("ukr")
fileComparCountry = get_data(comparCountry)

if fileUkraine and fileComparCountry:
  df_fileUkraine = pd.read_csv(fileUkraine, sep=";")
  df_fileComparCountry = pd.read_csv(fileComparCountry, sep=";")

  df_combine = pd.concat([df_fileUkraine, df_fileComparCountry], ignore_index=True)
  df_combine["Year"] = pd.to_numeric(df_combine["Year"])

  fig = px.line(
    df_combine,
    x="Year",
    y="Million",
    color="Country",
    markers=True,
  )
  fig.update_traces(line=dict(width=3))
  fig.update_layout(
    height=600,
    xaxis_title="Years",
    yaxis_title="Million",
    xaxis_tickangle=-75,
    xaxis=dict(dtick=1, range=[1990,2025]),
    margin=dict(l=100, r=20, t=100, b=80),
    title_font_textcase="upper",
    title=dict(
      text="Population, total",
      x=0.5,
      xanchor="center",
      y=0.9,
      yanchor="bottom",
      font=dict(color="#1b975a", size=18, weight="bold"),
    ),
    legend=dict(
      x=0.5,
      xanchor="center",
      y=-0.2,
      yanchor="top",
      orientation="h",
      font=dict(color="#880c77", size=16, weight="bold"),
    ),
  )
  fig.show()

else:
  print("Can`t found countries")


# TASK 3: Create bar

if fileComparCountry:
  df_country = pd.read_csv(fileComparCountry, sep=";")
  fig = px.bar(
    df_country,
    x="Year",
    y="Million",
    color="Country",
    text="Million",
  )
  fig.show()
else:
  print("Can`t find country file.")