import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Input and output file paths
input_file = 'input_data/NoDuplicates_Translated.csv'
output_file = 'output_data/tfidf_vectorized.csv'

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=10000, max_df=0.3, min_df=3)

# Process the CSV file in chunks
chunk_size = 1000  # Number of rows per chunk
is_first_chunk = True  # To handle header writing in the output file

for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    # Ensure the chunk has at least two columns
    if chunk.shape[1] < 2:
        raise ValueError("The input CSV must have at least two columns.")

    # Extract the first column and the second column
    first_col = chunk.iloc[:, 0]
    second_col = chunk.iloc[:, 1]

    # Vectorize the second column using TF-IDF
    tfidf_matrix = vectorizer.fit_transform(second_col)

    # Convert the TF-IDF matrix to a DataFrame
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    # Combine the first column with the TF-IDF DataFrame
    output_chunk = pd.concat([first_col.reset_index(drop=True), tfidf_df], axis=1)

    # Save the chunk to the output file
    output_chunk.to_csv(output_file, mode='a', index=False, header=is_first_chunk)
    is_first_chunk = False  # Only write the header for the first chunk