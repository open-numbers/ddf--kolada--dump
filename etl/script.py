import requests
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
KPI_LIST = [
    "N00923", "N00925", "N00959", "N01804", "N01805", "N01813", "N01817", "N01926", "N01950", "N01951", "N01953",
    "N01954", "N01956", "N01957", "N01961", "N02820", "N02822", "N02829", "N02832", "N02833", "N02834", "N02835",
    "N02836", "N02837", "N02838", "N02839", "N02840", "N02841", "N02842", "N02843", "N02844", "N02845", "N02846",
    "N02907", "N02908", "N02909", "N02910", "N02911", "N02913", "N02914", "N61924", "N61925", "N61980", "N61981",
    "N00905", "N00906", "N00914", "N00920", "N00924", "N00926", "N00968", "N00999", "N01006", "N01982", "N01984",
    "N02243", "N03932", "N31807", "N60802", "N60960", "N70832", "N70845", "N72826", "N72827", "N72828", "N72829",
    "N72830", "N72831", "N72832", "N72833", "N72834", "N72835", "N72836", "N72837", "N72848", "N72850", "N72851",
    "N72852", "N72855", "N72856", "N72857", "N72858", "N72859", "N74814", "N00564", "N00667", "N00905", "N01951",
    "N01958", "N02907", "N07001", "N07900", "N07901", "N07902", "N07903", "N07904", "N07907", "N07908", "N07909",
    "N07910", "N07911", "N07912", "N07913", "N07917", "N07923", "N07924", "N07925", "N07926", "N07927", "N07928",
    "N07929", "N45022", "U00958", "U30446", "U30464", "U30465", "N45900", "N45901", "N45904", "N45905", "N45910",
    "N45911", "N45912", "N45913", "N45914", "N45920", "N45925", "N45926", "N45927", "N45928", "N45933", "N45934",
    "N45970", "N45971", "N45972", "N45973", "N45974", "N45975", "N45976", "N45977", "N00097", "N00901", "N03002",
    "N03011", "N03034", "N03055", "N03102", "N03103", "N03105", "N03109", "N03112"
]
YEARS = range(1994, 2023)
BASE_URL = "https://api.kolada.se/v2/data/kpi/{}/year/{}"
REQUESTS_PER_SECOND = 5

def fetch_data(kpi, year):
    url = BASE_URL.format(kpi, year)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_and_save_data(kpi, data):
    file_name = f"ddf--datapoints--{kpi}--by--geo--year.csv"
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["geo", "year", kpi])
        for item in data.get('values', []):
            geo = item.get("municipality")
            if not geo.startswith("G"):  # Filter out municipalities starting with "G"
                year = item.get("period")
                for value in item.get("values", []):
                    if value.get("gender") == "T":
                        writer.writerow([geo, year, value.get("value")])
    print(f"Data for KPI {kpi} processed and saved.")

def main():
    with ThreadPoolExecutor(max_workers=REQUESTS_PER_SECOND) as executor:
        future_to_kpi_year = {
            executor.submit(fetch_data, kpi, year): (kpi, year)
            for kpi in KPI_LIST for year in YEARS
        }

        for future in as_completed(future_to_kpi_year):
            kpi, year = future_to_kpi_year[future]
            try:
                data = future.result()
                print(f"Fetched data for KPI {kpi} year {year}")
                process_and_save_data(kpi, data)
            except Exception as e:
                print(f"Error fetching data for KPI {kpi} year {year}: {e}")
            finally:
                time.sleep(1 / REQUESTS_PER_SECOND)

if __name__ == "__main__":
    print("Starting data fetching and processing...")
    main()
    print("Data fetching and processing completed.")
