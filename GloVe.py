import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def load_glove_embeddings(file_path):
    embeddings = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings
def get_glove_vector(token, embeddings, embedding_dim=100):
    return embeddings.get(token, np.zeros(embedding_dim))


def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.lower().split()
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

#GET DATA FROM DATAFRAME INTO A LIST - BUT JUST CONVERSATIONS SO THAT HUMAN AND CHATGPT ARENT INCLUDED 

df = pd.read_csv("/Users/dishita/Desktop/HumanFac/Dataframe_Wrangled_NoDuplicates.csv")
df['tokens'] = df['conversations'].apply(preprocess_text)

glove_embeddings_path = '/Users/dishita/Downloads/glove/glove.6B.100d.txt'  
glove_embeddings = load_glove_embeddings(glove_embeddings_path)


df['vectors'] = df['tokens'].apply(lambda tokens: [get_glove_vector(token, glove_embeddings) for token in tokens])
print("yay")

df.to_csv('vectorized_Glove.csv', index=False)

