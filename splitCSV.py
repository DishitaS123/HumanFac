import pandas as pd
import glob
import os

def merge_csv_files(input_dir, output_file):
    """Merges all CSV files in a directory into a single CSV file."""
    try:
        # Get a list of all CSV files in the directory
        csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

        if not csv_files:
            print(f"No CSV files found in '{input_dir}'")
            return

        # Read each CSV file into a DataFrame and append it to a list
        df_list = []
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            df_list.append(df)

        # Concatenate all DataFrames in the list into a single DataFrame
        merged_df = pd.concat(df_list, ignore_index=True)

        # Write the merged DataFrame to a new CSV file
        merged_df.to_csv(output_file, index=False)

        print(f"Successfully merged CSV files into '{output_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_directory = 'HumanFac/Datasets/csv_chunks'
output_csv = 'HumanFac/Datasets/merged_data_no_duplicates.csv'
merge_csv_files(input_directory, output_csv)