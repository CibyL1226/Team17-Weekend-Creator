import os
import pandas as pd

# Define the folder containing CSV files
folder_path = "Google_Places/google_csv"

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv("google_df.csv", index=False)

