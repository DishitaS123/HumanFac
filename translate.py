import pandas as pd
import re

csv_file_path = 'Datasets/Sample_Foreign_Language_Entry.csv'
df = pd.read_csv(csv_file_path)

# Function to split text so that every entry starts with 'from': 'human' or 'from': 'gpt'
def split_text(text):
    # Use regular expression to split based on 'from': 'human' or 'from': 'gpt'
    parts = re.split(r"(?=\{'from': 'human',|\{'from': 'gpt',)", text)
    # Filter out empty strings
    parts = [part for part in parts if part]
    return parts

# Apply the split_text function to the second column
df['split_text'] = df.iloc[:, 1].apply(split_text)

# Create a new DataFrame to store the results
split_df = pd.DataFrame()

# Add the key column
split_df['Key'] = df.iloc[:, 0]

# Add the split text columns
split_text_columns = pd.DataFrame(df['split_text'].tolist())
split_df = pd.concat([split_df, split_text_columns], axis=1)

# Save the new DataFrame to a new CSV file
output_csv_path = 'Datasets/Sample_Foreign_Language_Entry_Split.csv'
split_df.to_csv(output_csv_path, index=False)

print("Processing complete. Output saved to:", output_csv_path)