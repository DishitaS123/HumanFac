# Count the number of lines in the CSV file
file_path = 'HumanFac/Datasets/Dataframe_Combined_Wrangled.csv'

with open(file_path, 'r') as file:
    line_count = sum(1 for line in file) - 1  # Subtract 1 to exclude the header

print(f'Number of rows: {line_count}')