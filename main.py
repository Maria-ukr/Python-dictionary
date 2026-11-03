import requests
from requests.exceptions import HTTPError, Timeout
import pandas as pd
from pathlib import Path

params = {
  "date": "1991:2019",
  "format": "json",
  "per_page": "100",
}

country = "ukr"
indicator = "NY.GDP.PCAP.CD"

API_WORLD_URL = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}/"

file_name = Path(f"data_{country}.csv")

def get_data(url, params ={}) :
  try:
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    print("Data was successfully received")
    return response.json()
  except HTTPError as err:
    print(f"HTTP error: {err}")
    print(f"HTTP error: {err.response.status_code}")
  except Timeout: 
    print("Request timed out")
    
if not file_name.is_file():
  print(f"File {file_name} not exists !")
  recive_data = get_data(API_WORLD_URL, params)
  if recive_data and len(recive_data) > 1:
    data = pd.json_normalize(recive_data[1])
    print(f"Save file {file_name}")
    data.to_csv(file_name, index=False, sep=";")

if file_name.is_file():
  print(f"File {file_name} exists !")
  ukr_GDP = pd.read_csv(file_name, sep=";")
  ukr_GDP = ukr_GDP.rename(columns={"country.value": "country"})
  ukr_GDP = ukr_GDP.reset_index(drop=True)
  ukr_GDP["№"] = ukr_GDP.index + 1

# Copy file and filter columns to show
  file_copy = ukr_GDP.copy(deep=True)
  read_copy_data = pd.DataFrame(file_copy)

# Calculate average GDP
  aver_GDP = read_copy_data["value"].mean()

# Years when GDP reduced compared to the previous year
  read_copy_data["is_reduce"] = (read_copy_data["value"] > read_copy_data["value"].shift(-1))

# Year of the MAX / MIN of GDP
  max_GDP = read_copy_data.loc[read_copy_data["value"].idxmax()]
  min_GDP = read_copy_data.loc[read_copy_data["value"].idxmin()]

  summary_rows = pd.DataFrame([
    {"№": ""},
    {"№": "", "country": "Average GDP", "value": aver_GDP},
    {"№": "", "country": f"Max GDP - {max_GDP["date"]}", "value": max_GDP["value"]},
    {"№": "", "country": f"Min GDP - {min_GDP["date"]}", "value": min_GDP["value"]},
  ])

# Save the copy of the data with selected columns
  columns_to_show = ["№", "country", "date", "value", "is_reduce"]
  read_copy_data.to_csv(f"{file_name}_copy.csv", columns=columns_to_show, index=False, sep=";")

# Save the result data with summary rows
  result_data = pd.concat([read_copy_data, summary_rows], ignore_index=True)

  result_data.to_csv(f"{file_name}_result.csv", columns=columns_to_show, index=False, sep=";")
  print(f"Save file {file_name}_result.csv")
  print(pd.read_csv(f"{file_name}_result.csv", usecols=["country", "value"], sep=";").tail(3))