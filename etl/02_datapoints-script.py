import requests
import csv
import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
KPI_LIST = [ "n00300"]


YEARS = range(1994, 2023)
BASE_URL = "https://api.kolada.se/v2/data/kpi/{}/year/{}"
REQUESTS_PER_SECOND = 10
DATAPOINTS_GEO_YEAR_DIR = "datapoints--by--geo--year"
DATAPOINTS_GEO_GENDER_YEAR_DIR = "datapoints--by--geo--gender--year"
LOG_FILE = "datapoints_log.txt"

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def fetch_data(kpi, year):
    url = BASE_URL.format(kpi, year)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_and_save_data(kpi, data):
    file_name = f"{DATAPOINTS_GEO_YEAR_DIR}/ddf--datapoints--{kpi.lower()}--by--geo--year.csv"
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["geo", "year", kpi.lower()])
        for item in data.get('values', []):
            geo = item.get("municipality")
            if not geo.startswith("G"):  # Filter out municipalities starting with "G"
                year = item.get("period")
                for value in item.get("values", []):
                    if value.get("gender") == "T":
                        writer.writerow([geo, year, value.get("value")])

    file_name = f"{DATAPOINTS_GEO_GENDER_YEAR_DIR}/ddf--datapoints--{kpi.lower()}--by--geo--gender--year.csv"
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["geo", "gender", "year", kpi.lower()])
        for item in data.get('values', []):
            geo = item.get("municipality")
            if not geo.startswith("G"):  # Filter out municipalities starting with "G"
                year = item.get("period")
                for value in item.get("values", []):
                    gender = value.get("gender")
                    if gender in ("K", "M"):
                        writer.writerow([geo, gender.lower(), year, value.get("value")])
    logging.info(f"Data for KPI {kpi} processed and saved.")

def main():
    # Ensure datapoints directory exists
    os.makedirs(DATAPOINTS_GEO_YEAR_DIR, exist_ok=True)
    os.makedirs(DATAPOINTS_GEO_GENDER_YEAR_DIR, exist_ok=True)

    with ThreadPoolExecutor(max_workers=1) as executor:
        future_to_kpi_year = {
            executor.submit(fetch_data, kpi, year): (kpi, year)
            for kpi in KPI_LIST for year in YEARS
        }

        for future in as_completed(future_to_kpi_year):
            kpi, year = future_to_kpi_year[future]
            try:
                data = future.result()
                logging.info(f"Fetched data for KPI {kpi} year {year}")
                print(f"Fetched data for KPI {kpi} year {year}")
                process_and_save_data(kpi, data)
            except Exception as e:
                logging.error(f"Error fetching data for KPI {kpi} year {year}: {e}")
                print.error(f"Error fetching data for KPI {kpi} year {year}: {e}")
            finally:
                time.sleep(1 / REQUESTS_PER_SECOND)

if __name__ == "__main__":
    logging.info("Starting data fetching and processing...")
    main()
    logging.info("Data fetching and processing completed.")
