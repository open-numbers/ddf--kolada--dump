import csv
import os
import sys

def process_csv(file_path, key_columns):
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = list(reader)

        # Determine key and non-key columns based on the number of key columns provided
        key_indices = range(key_columns)
        non_key_indices = range(key_columns, len(headers))

        # Use a dictionary to ensure uniqueness of key column combinations
        unique_rows = {}
        empty_values_removed = 0
        duplicate_keys_removed = 0

        for row in data:
            key = tuple(row[index] for index in key_indices)  # Create a tuple of key column values
            non_key = [row[index] for index in non_key_indices]  # List of non-key column values
            
            # Check for empty values in non-key columns and skip those rows
            if any(not cell.strip() for cell in non_key):
                empty_values_removed += 1
                continue
            
            # Check for duplicate keys and keep the first occurrence
            if key in unique_rows:
                duplicate_keys_removed += 1
                continue
            
            unique_rows[key] = row

        # Write the unique rows back to the file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(unique_rows.values())

        return len(data) - len(unique_rows), empty_values_removed, duplicate_keys_removed

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def process_folder(folder_path, key_columns):
    csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
    total_removed = 0

    log_entries = []

    for file in csv_files:
        result = process_csv(file, key_columns)
        if result:
            removed, empty_removed, duplicates_removed = result
            total_removed += removed
            log_entries.append(f"{os.path.basename(file)}: Total removed = {removed}, Empty values removed = {empty_removed}, Duplicates removed = {duplicates_removed}")

    # Print and save log
    log_path = os.path.join(folder_path, 'process_log.txt')
    with open(log_path, mode='w') as log_file:
        log_file.write('\n'.join(log_entries))
    
    print(f"Processed {len(csv_files)} files. Total rows removed: {total_removed}. Detailed log saved to {log_path}.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <folder_path> <number_of_key_columns>")
        sys.exit(1)

    folder_path = sys.argv[1]
    key_columns = int(sys.argv[2])
    process_folder(folder_path, key_columns)
