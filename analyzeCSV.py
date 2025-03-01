import pandas as pd
import pandas as pd

def copy_first_5_rows(input_file, output_file):
    """Reads the first 5 rows of a CSV and writes them to a new CSV."""
    try:
        # Read the first 5 rows into a pandas DataFrame
        df = pd.read_csv(input_file, nrows=5)

        # Write the DataFrame to a new CSV file
        df.to_csv(output_file, index=False)  # index=False prevents writing row indices

        print(f"Successfully copied the first 5 rows to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_csv = 'HumanFac/Datasets/Dataframe_Wrangled_part1.csv'  # Replace with your input file path
output_csv = 'output.csv' # Replace with your output file path
copy_first_5_rows(input_csv, output_csv)