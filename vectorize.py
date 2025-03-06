import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import csv

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to split text into chunks
def split_text(text, max_length):
    tokens = tokenizer.tokenize(text)
    chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
    return chunks

# Function to vectorize text using BERT
def vectorize_text(text):
    max_length = 510  # Account for [CLS] and [SEP] tokens
    chunks = split_text(text, max_length)
    embeddings = []
    
    for chunk in chunks:
        inputs = tokenizer.encode_plus(chunk, return_tensors='pt', truncation=True, padding='max_length', max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
    
    # Aggregate embeddings (e.g., by averaging)
    aggregated_embedding = sum(embeddings) / len(embeddings)
    return aggregated_embedding

# Read the CSV file
input_csv_path = 'Datasets/Dataframe_Wrangled_NoDuplicates.csv'  # Replace with your input CSV file path
df = pd.read_csv(input_csv_path)

# Open the output CSV file in write mode
output_csv_path = 'Datasets/BERT_Output.csv'  # Replace with your output CSV file path
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['original_text', 'vectorized'])

    # Process each row and write to the output CSV file
    for index, row in df.iterrows():
        original_text = row[1]
        vectorized = vectorize_text(original_text)
        writer.writerow([original_text, vectorized.tolist()])
        print(f'Processed row {index + 1}/{len(df)}')

print("Processing complete. Output saved to:", output_csv_path)