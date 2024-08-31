import csv
import os
import sys

def make_lowercase_in_csv(file_path):
    try:
        # Read the CSV file and convert each value to lowercase
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            data = [[cell.lower() for cell in row] for row in reader]

        # Write the modified data back to the file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return True  # Return True to indicate success

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False  # Return False to indicate failure

def process_folder(folder_path):
    # List all CSV files in the given folder
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Summary counters
    processed_count = 0
    error_count = 0

    # Process each file
    for file in csv_files:
        result = make_lowercase_in_csv(file)
        if result:
            processed_count += 1
        else:
            error_count += 1

    # Print summary
    print(f"Processed {processed_count} files successfully.")
    print(f"Encountered errors in {error_count} files.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)
