import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
from sklearn.feature_extraction.text import TfidfVectorizer

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


# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Split the data into 20 parts
num_parts = 20
dfs = np.array_split(df, num_parts)

# Initialize an empty list to store the TF-IDF matrices
tfidf_matrices = []

# Fit and transform each part of the dataframe
for i, part in enumerate(dfs):
    tfidf_matrix_part = tfidf_vectorizer.fit_transform(part.iloc[:, 1])
    tfidf_matrices.append(torch.tensor(tfidf_matrix_part.toarray()))
    print(f"Part {i+1} vectorized")

# Combine the TF-IDF matrices
tfidf_matrix = torch.vstack(tfidf_matrices)
tfidf_matrix = tfidf_vectorizer.fit_transform(df.iloc[:, 1])
# Convert the TF-IDF matrix to a dense format and create a DataFrame
tfidf_dense = tfidf_matrix.todense()
tfidf_df = pd.DataFrame(tfidf_dense)

# Save the DataFrame with TF-IDF vectors to a CSV file
output_file_path = 'HumanFac/Datasets/Dataframe_With_TFIDF_Vectors.csv'
tfidf_df.to_csv(output_file_path, index=False)
print("Output file saved to:", output_file_path)


# # Load pre-trained BERT model and tokenizer
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained('bert-base-uncased')

# # Function to vectorize text using BERT
# def bert_vectorize(text):
#     inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
#     outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# # Apply BERT vectorization to each entry in the dataframe
# df['bert_vector'] = df.iloc[:, 1].apply(bert_vectorize)

# # Display the first few rows of the dataframe with BERT vectors
# print(df.head())

# # Save the dataframe with BERT vectors to a CSV file
# output_file_path = 'HumanFac/Datasets/Dataframe_With_BERT_Vectors.csv'
# df.to_csv(output_file_path, index=False)