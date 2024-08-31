import csv
import os
import sys

def delete_empty_csv_files(folder_path):
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    deleted_files = []

    for file_path in csv_files:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        # Check if the file has only the header or no rows at all
        if len(rows) <= 1:
            os.remove(file_path)
            deleted_files.append(os.path.basename(file_path))

    return deleted_files

def main(folder_path):
    deleted_files = delete_empty_csv_files(folder_path)
    
    if deleted_files:
        print(f"Deleted {len(deleted_files)} empty files:")
        for file in deleted_files:
            print(f"- {file}")
    else:
        print("No empty files found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    main(folder_path)
