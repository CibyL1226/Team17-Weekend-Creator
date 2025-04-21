import os
import json
import pandas as pd

folder_path = "Google_Places" 

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing {file_path}...")

        with open(file_path, "r") as f:
            data = json.load(f)

        df = pd.json_normalize(data)


        csv_filename = filename.replace(".json", ".csv")
        csv_path = os.path.join(folder_path, csv_filename)
        df.to_csv(csv_path, index=False)

        print(f"Saved CSV: {csv_path}")


input_folder = "Google_Places" 
output_folder = os.path.join(input_folder, "google_csv")

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        print(f"Processing {file_path}...")

        with open(file_path, "r") as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        csv_filename = filename.replace(".json", ".csv")
        csv_path = os.path.join(output_folder, csv_filename)
        df.to_csv(csv_path, index=False)

        print(f"Saved CSV: {csv_path}")
