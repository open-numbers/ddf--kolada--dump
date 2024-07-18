import os
import csv

def lowercase_headers_in_csv(file_path):
    # Read the CSV file
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    if not rows:
        print(f"File {file_path} is empty.")
        return
    
    # Convert headers to lowercase
    headers = [header.lower() for header in rows[0]]
    rows[0] = headers
    
    # Write the CSV file back
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Headers in file {file_path} have been converted to lowercase.")

def process_all_csv_files(directory):
    # Iterate over all CSV files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            lowercase_headers_in_csv(file_path)
            new_file_name = file_name.lower()
            new_file_path = os.path.join(directory, new_file_name)
            os.rename(file_path, new_file_path)
            print(f"File {file_name} has been renamed to {new_file_name}.")

if __name__ == "__main__":
    directory = "./"  # Specify your directory containing the CSV files here
    print(f"Processing all CSV files in directory: {directory}")
    process_all_csv_files(directory)
    print("Processing completed.")
