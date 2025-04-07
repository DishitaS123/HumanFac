import csv
import json
import sys
import pandas as pd

def read_ids_from_csv(file_path):
    csv.field_size_limit(sys.maxsize)
    ids = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        df = pd.read_csv(file_path)
        ids = df.iloc[:, 0].tolist()  # Assuming 'id' is the first column
    return ids


def get_rows_from_json(file_paths, ids):
    rows = []
    all_data = []  # List to store data from all JSON files

    # Load all JSON files into memory
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)  # Load the entire JSON file as a single object
                all_data.extend(data)  # Add the data to the combined list
        except Exception as e:
            print(f"Error reading JSON file {file_path}: {e}")


    for id in ids:
        isfound = False
        for item in all_data:  # Iterate through the combined JSON data
            if item['id'] == id:  # Check if the item's ID matches
                rows.append(item)
                isfound = True
                break  # Stop searching once the ID is found
        if not isfound:
            print(f"ID {id} not found in any JSON file.")

    return rows
                
                




def save_new_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Example usage
# file_path = 'relevant_rows_summarized_output.csv'
# ids = read_ids_from_csv(file_path)

def extract_ids_from_csv(file_path):
    ids = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            ids.append(row[0])  # Assuming 'id' is the first column
    return ids


json_paths = ['sg_90k_part1.json', 'sg_90k_part2.json']

# Example usage
nick_csv_file_path = 'relevant_rows_summarized_output.csv'
michelle_csv_file_path = 'lda_relevant_conversations_no_duplicates.csv'

dashita_ids = ['0g9h3C1', 'Cxw9BrT', 'c1VfpQq', '1aiwVCg', 'wNBG8Gp', 'mfi8wDB', 'HSJi4eb', 'efcAzKB', 'cEFR8NE', 'RGc8dqu', 'iVqSurZ', 'RGc8dqu', 'ORDEfFm', 'Km9Mf8E', 'kTsaxCJ', 'lih8Bud', 'VXmLZLH', 'DqOywni']

failing_ids = ['0g9h3C1', 'ORDEfFm', 'iVqSurZ']
corrected_ids = ['Og9h3C1', '0RDEfFm', 'ivqSurZ']

dashita_corrected_ids = ['Og9h3C1', 'Cxw9BrT', 'c1VfpQq', '1aiwVCg', 'wNBG8Gp', 'mfi8wDB', 'HSJi4eb', 'efcAzKB', 'cEFR8NE', 'RGc8dqu', 'ivqSurZ', 'RGc8dqu', '0RDEfFm', 'Km9Mf8E', 'kTsaxCJ', 'lih8Bud', 'VXmLZLH', 'DqOywni']


nick_ids = read_ids_from_csv(nick_csv_file_path)
michelle_ids = read_ids_from_csv(michelle_csv_file_path)

# Combine the ID lists using a set to ensure uniqueness
combined_ids = set(dashita_corrected_ids + nick_ids + michelle_ids)

# Convert the set back to a list if needed
ids = list(combined_ids)

relevant_rows = get_rows_from_json(json_paths, ids)

print(f"Number of entries in the JSON file: {len(relevant_rows)}")

save_new_json('relevant_rows.json', relevant_rows)

# # Write the IDs to a TXT file
# output_txt_file = 'unique_ids.txt'
# with open(output_txt_file, mode='w', encoding='utf-8') as txtfile:
#     for id in ids:
#         txtfile.write(f"{id}\n")

# # Calculate the number of duplicates
# total_ids = len(dashita_ids) + len(nick_ids) + len(michelle_ids)
# unique_ids = len(combined_ids)
# duplicates_count = total_ids - unique_ids

# # Print the number of duplicates
# print(f"Number of duplicates found: {duplicates_count}")

# print(len(ids))
# # print(f"Total number of unique IDs: {unique_ids}")

# # json_file_path = 'sg_90k_part1.json'
# # rows = get_rows_from_json(json_file_path, ids)
# # print(rows)
# # save_new_json('relevant_rows.json', rows)
