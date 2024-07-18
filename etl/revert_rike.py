import os
import csv

def remove_leading_zeros_and_fix_geo(file_path):
    # Read the CSV file
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    if not rows:
        print(f"File {file_path} is empty.")
        return
    
    # Check if "geo" is in headers
    headers = rows[0]
    if "geo" not in headers:
        print(f"File {file_path} does not contain 'geo' column.")
        return
    
    # Get the index of "geo" column
    geo_index = headers.index("geo")
    
    # Remove leading zeros in "geo" column and fix missing values
    for row in rows[1:]:
        geo_value = row[geo_index].lstrip('0')
        if geo_value == "":
            geo_value = "0"
        row[geo_index] = geo_value
    
    # Write the CSV file back
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Processed file {file_path}: removed leading zeros and fixed missing 'geo' values.")

def process_all_csv_files(directory):
    # Iterate over all CSV files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            remove_leading_zeros_and_fix_geo(file_path)

if __name__ == "__main__":
    directory = "./"  # Specify your directory containing the CSV files here
    print(f"Processing all CSV files in directory: {directory}")
    process_all_csv_files(directory)
    print("Processing completed.")
