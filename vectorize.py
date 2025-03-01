import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import vstack
import os


# Input file path
file_path_1 = 'HumanFac/Datasets/Dataframe_Wrangled_part1.csv'

# Output directory
output_dir = 'HumanFac/Datasets/TFIDF_Chunks'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Chunk size
chunk_size = 100

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Read the CSV file in chunks
chunk_number = 0
for chunk in pd.read_csv(file_path_1, chunksize=chunk_size):
    chunk_number += 1
    # Vectorize the text column
    tfidf_matrix = tfidf_vectorizer.fit_transform(chunk.iloc[:, 1])

    # Create a DataFrame from the TF-IDF matrix
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

    # Create the output file path
    output_file_path = os.path.join(output_dir, f'tfidf_chunk_{chunk_number}.csv')

    # Save the DataFrame to a CSV file
    tfidf_df.to_csv(output_file_path, index=False)
    print(f"Chunk {chunk_number} saved to: {output_file_path}")

print("All chunks processed and saved.")

#transform the rest of the data.
chunk_number = 0;
for chunk in pd.read_csv('HumanFac/Datasets/Dataframe_Wrangled_part2.csv', chunksize=chunk_size):
    chunk_number += 1;
    tfidf_matrix = tfidf_vectorizer.transform(chunk.iloc[:,1])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    output_file_path = os.path.join(output_dir, f'tfidf_chunk_part2_{chunk_number}.csv')
    tfidf_df.to_csv(output_file_path, index=False)
    print(f"part 2, Chunk {chunk_number} saved to: {output_file_path}")
print("part 2 chunks finished")

# # Input file path
# file_path_1 = 'HumanFac/Datasets/Dataframe_Wrangled_part1.csv'

# # Output file path
# output_file_path = 'HumanFac/Datasets/Dataframe_With_TFIDF_Vectors.csv'

# # Initialize TF-IDF Vectorizer
# tfidf_vectorizer = TfidfVectorizer()

# # Read only the first row from the CSV file
# df = pd.read_csv(file_path_1, nrows=1)

# # Extract the text from the specified column (assuming it's the second column, index 1)
# text = df.iloc[0, 1]

# # Vectorize the text
# tfidf_matrix = tfidf_vectorizer.fit_transform([text])  # Note: fit_transform expects a list of strings

# # Convert the TF-IDF matrix to a dense DataFrame
# tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# # Save the DataFrame to a CSV file
# tfidf_df.to_csv(output_file_path, index=False)
# print("Output file saved to:", output_file_path)
# print("Shape of TFIDF dataframe: ", tfidf_df.shape)


# # Input file paths
# file_path_1 = 'HumanFac/Datasets/Dataframe_Wrangled_part1.csv'
# file_path_2 = 'HumanFac/Datasets/Dataframe_Wrangled_part2.csv'

# # Output file path
# output_file_path = 'HumanFac/Datasets/Dataframe_With_TFIDF_Vectors.csv'

# # Chunk size (adjust as needed)
# chunk_size = 1000

# # Initialize TF-IDF Vectorizer
# tfidf_vectorizer = TfidfVectorizer()

# # Lists to store chunks of TF-IDF vectors
# tfidf_chunks = []

# # Process the first file in chunks
# first_chunk = True
# for chunk in pd.read_csv(file_path_1, chunksize=chunk_size):
#     if first_chunk:
#         tfidf_matrix_chunk = tfidf_vectorizer.fit_transform(chunk.iloc[:, 1])
#         first_chunk = False
#     else:
#         tfidf_matrix_chunk = tfidf_vectorizer.transform(chunk.iloc[:, 1])
#     tfidf_chunks.append(tfidf_matrix_chunk)

# # Process the second file in chunks
# for chunk in pd.read_csv(file_path_2, chunksize=chunk_size):
#     tfidf_matrix_chunk = tfidf_vectorizer.transform(chunk.iloc[:, 1])
#     tfidf_chunks.append(tfidf_matrix_chunk)

# # Vertically stack the TF-IDF matrices (using scipy.sparse.vstack)
# tfidf_matrix = vstack(tfidf_chunks)

# # Create a DataFrame from the combined TF-IDF matrix
# tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# # Save the DataFrame to a CSV file
# tfidf_df.to_csv(output_file_path, index=False)
# print("Output file saved to:", output_file_path)
# print("Shape of TFIDF dataframe: ", tfidf_df.shape)

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