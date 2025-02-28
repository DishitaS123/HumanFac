import pandas as pd
from transformers import BertTokenizer, BertModel
import torch

# Load data from CSV file into a pandas dataframe
#file_path = 'HumanFac/Datasets/Dataframe_Combined_Wrangled.csv'
file_path = 'HumanFac/Datasets/Dataframe_Wrangled_part1.csv'
df1 = pd.read_csv(file_path)
# Load data from a second CSV file into another pandas dataframe
file_path_2 = 'HumanFac/Datasets/Dataframe_Wrangled_part2.csv'
df2 = pd.read_csv(file_path_2)

# Concatenate the two dataframes
df = pd.concat([df1, df2], ignore_index=True)


# Display the first few rows of the dataframe
print(df.head())
print(df.iloc[0, 1])
print(len(df.iloc[0]))

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to vectorize text using BERT
def bert_vectorize(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Apply BERT vectorization to each entry in the dataframe
df['bert_vector'] = df.iloc[:, 1].apply(bert_vectorize)

# Display the first few rows of the dataframe with BERT vectors
print(df.head())

# Save the dataframe with BERT vectors to a CSV file
output_file_path = 'HumanFac/Datasets/Dataframe_With_BERT_Vectors.csv'
df.to_csv(output_file_path, index=False)