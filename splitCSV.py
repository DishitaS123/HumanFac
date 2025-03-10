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


def split_csvs(input_csv, output_dir):
    """Splits a CSV file into multiple CSV files, each with 100 lines."""
    try:
        # Read the input CSV file into a DataFrame
        df = pd.read_csv(input_csv)

        # Determine the number of output files needed
        num_files = len(df) // 100 + (1 if len(df) % 100 != 0 else 0)

        # Split the DataFrame into chunks of 100 rows each
        for i in range(num_files):
            start_row = i * 100
            end_row = start_row + 100
            chunk_df = df[start_row:end_row]

            # Define the output file path
            output_file = os.path.join(output_dir, f"chunk_{i+1}.csv")

            # Write the chunk DataFrame to a new CSV file
            chunk_df.to_csv(output_file, index=False)

        print(f"Successfully split '{input_csv}' into {num_files} files in '{output_dir}'")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# input_directory = 'HumanFac/Datasets/csv_chunks'
# output_csv = 'HumanFac/Datasets/merged_data_no_duplicates.csv'
# merge_csv_files(input_directory, output_csv)

input_csv = 'Datasets/Dataframe_Wrangled_NoDuplicates.csv'
output_directory = 'Datasets/Split_CSV'
split_csvs(input_csv, output_directory)