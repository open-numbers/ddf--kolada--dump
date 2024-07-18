import os
import csv
from collections import defaultdict

def remove_duplicates_and_check_conflicts(file_path):
    unique_rows = {}
    conflicts = defaultdict(list)
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    if not rows:
        print(f"File {file_path} is empty.")
        return
    
    headers = rows[0]
    geo_index = headers.index("geo")
    year_index = headers.index("year")
    
    for row in rows[1:]:
        geo = row[geo_index]
        year = row[year_index]
        key = (geo, year)
        
        if key in unique_rows:
            if unique_rows[key] != row:
                conflicts[key].append(unique_rows[key])
                conflicts[key].append(row)
        else:
            unique_rows[key] = row
    
    if conflicts:
        print(f"Conflicts found in file {file_path}:")
        for key, conflict_rows in conflicts.items():
            print(f"Conflict for geo={key[0]} and year={key[1]}:")
            for conflict_row in conflict_rows:
                print(conflict_row)
    
    # Write the unique rows back to the CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(unique_rows.values())
    
    print(f"Processed file {file_path} with unique rows and conflicts checked.")

def process_all_csv_files(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            remove_duplicates_and_check_conflicts(file_path)

if __name__ == "__main__":
    directory = "./"  # Specify your directory containing the CSV files here
    print(f"Processing all CSV files in directory: {directory}")
    process_all_csv_files(directory)
    print("Processing completed.")
