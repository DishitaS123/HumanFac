import pandas as pd
import csv
import re
import unicodedata
from googletrans import Translator
import asyncio


# Function to clean and normalize text
def clean_text(text):
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

# Asynchronous function to translate text to English
async def translate_to_english(text):
    translator = Translator()
    translated = await translator.translate(text, dest='en')
    return translated.text

# # Asynchronous function to translate a list of texts
# async def translate_list(text_list):
#     tasks = [translate_to_english(text) for text in text_list]
#     return await asyncio.gather(*tasks)


# Function to split text so that every entry starts with 'from': 'human' or 'from': 'gpt'
def split_text(text):
    text = clean_text(text)
    # Use regular expression to split based on 'from': 'human' or 'from': 'gpt'
    parts = re.split(r"(?=\{'from': 'human',|\{'from': 'gpt',)", text)
    # Filter out empty strings
    parts = []
    for part in re.split(r"(?=\{'from': 'human',|\{'from': 'gpt',)", text):
        if part:
            translated_part = asyncio.run(translate_to_english(part))
            parts.append(translated_part)
    return parts

# Asynchronous function to process and translate each row
def process_and_translate_row(row):
    first_col = row[0]
    translated_texts = []
    for col in row[1:]:
        split_texts = split_text(str(col))
        translated_texts.append(' '.join(split_texts))
    return [first_col] + translated_texts

def split_and_save_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)

    # Open the output CSV file in write mode
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        header = ['first_col'] + [f'vectorized_col_{i}' for i in range(1, len(df.columns))]
        writer.writerow(header)

        # Process each row and write to the output CSV file
        for index, row in df.iterrows():
            translated_row = process_and_translate_row(row)
            writer.writerow(translated_row)
            print(f'Processed row {index + 1}/{len(df)}')

    print("Processing complete. Output saved to:", output_csv_path)

input_csv_path = 'Datasets/Dataframe_Wrangled_NoDuplicates.csv'
output_csv_path = 'Datasets/NoDuplicates_Translated.csv'
split_and_save_csv(input_csv_path, output_csv_path)


