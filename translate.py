import pandas as pd
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

def split_and_save_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)

    # Apply the split_text function to the second column
    df['split_text'] = df.iloc[:, 1].apply(split_text)

    print(df['split_text'].head())

    # Create a new DataFrame to store the results
    split_df = pd.DataFrame()

    # Add the key column
    split_df['Key'] = df.iloc[:, 0]

    print(split_df.head())

    # Add the split text columns
    split_text_columns = pd.DataFrame(df['split_text'])

    print(split_text_columns)

    
    split_df = pd.concat([split_df, split_text_columns], axis=1)

    # Save the new DataFrame to a new CSV file
    split_df.to_csv(output_csv_path, index=False)

    print("Splitting into conversations complete. Output saved to:", output_csv_path)

input_csv_path = 'Datasets/Dataframe_Wrangled_NoDuplicates.csv'
output_csv_path = 'Datasets/NoDuplicates_Translated.csv'
split_and_save_csv(input_csv_path, output_csv_path)


