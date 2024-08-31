import csv
import os
import json
import sys

def generate_json_for_csv_files(folder_path):
    resources = []
    ddf_schema = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            relative_path = os.path.relpath(file_path, start=folder_path)  # Make path relative to folder
            name_without_extension = os.path.splitext(filename)[0]
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Assume the first row contains headers

            # Determine schema
            fields = [{"name": header} for header in headers]
            primary_key = ["geo", "year"] + (["gender"] if "gender" in headers else [])
            last_column_header = headers[-1]

            resources.append({
                "name": name_without_extension,
                "path": relative_path.replace('../', ''),  # Avoid any '../' in the path
                "schema": {
                    "fields": fields,
                    "primaryKey": primary_key
                }
            })

            ddf_schema.append({
                "primaryKey": primary_key,
                "value": last_column_header,
                "resources": [name_without_extension]
            })

    # Sort resources by 'name' and ddf_schema by 'value'
    resources.sort(key=lambda x: x['name'])
    ddf_schema.sort(key=lambda x: x['value'])

    # Save resources.json
    with open(os.path.join(folder_path, 'resources.json'), 'w') as f:
        json.dump(resources, f, indent=4)

    # Save ddfSchema.json
    with open(os.path.join(folder_path, 'ddfSchema.json'), 'w') as f:
        json.dump(ddf_schema, f, indent=4)

    print(f"Generated resources.json and ddfSchema.json in {folder_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    generate_json_for_csv_files(folder_path)
