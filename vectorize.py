import pandas as pd
from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to vectorize text using BERT
def vectorize_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Read the CSV file
input_csv_path = 'HumanFac/Datasets/Dataframe_Wrangled_NoDuplicates.csv'  # Replace with your input CSV file path
df = pd.read_csv(input_csv_path)

# Vectorize the second column
df['vectorized'] = df.iloc[:, 1].apply(vectorize_text)

# Save the new DataFrame to a new CSV file
output_csv_path = 'HumanFac/Datasets/BERT_Output.csv'  # Replace with your output CSV file path
df.to_csv(output_csv_path, index=False)