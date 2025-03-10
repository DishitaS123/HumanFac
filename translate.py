import pandas as pd
import csv
import re
import os
import unicodedata
import time
import random
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
    try:
        translator = Translator()
        translated = await translator.translate(text, dest='en')
        return translated.text
    except Exception as e:
        print(f"Error translating text: {e}")
        print(f"Sleeping for {60} seconds")
        time.sleep(60)
        return await translate_to_english(text)

# # Asynchronous function to translate a list of texts
# async def translate_list(text_list):
#     tasks = [translate_to_english(text) for text in text_list]
#     return await asyncio.gather(*tasks)


# Function to split text so that every entry starts with 'from': 'human' or 'from': 'gpt'
def split_text(text):
    text = clean_text(text)
    # Use regular expression to split based on 'from': 'human' or 'from': 'gpt'
    inital_parts = re.split(r"(?=\{'from': 'human',|\{'from': 'gpt',)", text)
    # Filter out empty strings
    parts = []
    # print(f"{len(inital_parts)} parts in intial split")
    for part in re.split(r"(?=\{'from': 'human',|\{'from': 'gpt',)", text):
        if part:
            chunks = []
            if(len(part) > 5000):
                chunks = [part[i:i+5000] for i in range(0, len(part), 5000)]
                # print(f"splitting into {len(chunks)} chunks")
            else:
                chunks = [part]

            translated_result = ""

            for chunk in chunks:
                translated_chunk = asyncio.run(translate_to_english(chunk))
                translated_result += translated_chunk
            #time.sleep(30) #30 second pause
            # translated_part = asyncio.run(translate_to_english(part))
            parts.append(translated_result)
    return parts

# Asynchronous function to process and translate each row
def process_and_translate_row(row):
    first_col = row[0]
    translated_texts = []
    # print(f"Splitting row into {len(row[1:])} parts")
    for col in row[1:]:
        split_texts = split_text(str(col))
        translated_texts.append(' '.join(split_texts))
    return [first_col] + translated_texts

def split_and_save_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)

    # Open the output CSV file in write mode
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
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

def eliminate_english(input_csv_path, elim_output_path):
    df = pd.read_csv(input_csv_path)

    # parse conversations
    text_list = []
    text_arrays = []
    for conversation in df["conversations"]:
        text = ""
        text_arr = []
        parsed_conversation = eval(conversation)
        for dialogue in parsed_conversation:
            text += dialogue["value"] + " "
            text_arr.append(dialogue["value"])
        text_list.append(text)
        text_arrays.append(text_arr)

    # create column with the conversation text
    df["text"] = text_list
    df["values"] = text_arrays

input_csv_path = 'Datasets/Dataframe_Wrangled_NoDuplicates.csv'
output_csv_path = 'Datasets/NoDuplicates_Translated.csv'
split_and_save_csv(input_csv_path, output_csv_path)

# for file in os.listdir('Datasets/Split_CSV'):
#     input_csv_path = f'Datasets/Split_CSV/{file}'
#     output_csv_path = f'Datasets/Split_CSV_Translated/{file}'
#     split_and_save_csv(input_csv_path, output_csv_path)
#     time.sleep(60)
#     print(f"Sleeping for {60} seconds")
