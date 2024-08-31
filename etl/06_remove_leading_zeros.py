import os
import csv
import sys

def process_geo_value(geo_value):
    # Check if geo is 4 characters long and contains only digits
    if len(geo_value) != 4 or not geo_value.isdigit():
        raise ValueError(f"Invalid geo value: {geo_value}. Must be a 4-character string of digits.")
    
    # Apply the transformation rules
    if geo_value == '0000':
        return '0'
    elif geo_value.startswith('000') and geo_value[3] != '0':
        return geo_value[2:]  # 000y -> 0y
    elif geo_value.startswith('00') and geo_value[2] != '0':
        return geo_value[2:]  # 00yx -> yx
    elif geo_value.startswith('0') and geo_value[1] != '0':
        return geo_value  # 0axx -> no modification (leading 0 is preserved)
    else:
        return geo_value  # axxx -> no modification (no leading zero)

def remove_leading_zeros_in_geo(file_path):
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
    
    # Get the index of the "geo" column
    geo_index = headers.index("geo")
    
    # Process "geo" values
    for row in rows[1:]:
        original_geo = row[geo_index]
        try:
            row[geo_index] = process_geo_value(original_geo)
        except ValueError as e:
            print(f"Error in file {file_path}: {e}")
            sys.exit(1)  # Stop execution if invalid geo value is found

    # Write the CSV file back
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Processed file {file_path}: 'geo' values have been adjusted.")

def process_all_csv_files(directory):
    # Iterate over all CSV files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            remove_leading_zeros_in_geo(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)
        
    directory = sys.argv[1]  # Specify your directory containing the CSV files here
    print(f"Processing all CSV files in directory: {directory}")
    process_all_csv_files(directory)
    print("Processing completed.")
