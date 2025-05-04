import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from collections import Counter

#load in stopwords
nltk.download('stopwords')

#FUNCTIONS--------------------------------------------------------------------------

#preprocess conversations data:
def preprocess_text(text):
    #remove punctuation:
    text = re.sub(r'[^\w\s]', '', text)
    words = text.lower().split()
    #remove stopwords from the text
    stop_words = set(stopwords.words('english'))
    new_words = []
    for word in words:
        if word not in stop_words:
            new_words.append(word)
    return new_words

#load glove embeddings from vocab file:
def load_glove_vocab(glove_embeddings_path):
    glove_vocab_matrix = {}
    with open(glove_embeddings_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype='float32')
            glove_vocab_matrix[word] = vector
    return glove_vocab_matrix

#create embeddings for the conversations:
def create_embeddings(conversations, glove_vocab):
    embeddings = []
    for conversation in conversations:
        # initialize a vector of zeros
        vector = np.zeros(next(iter(glove_vocab.values())).shape)  
        count = 0
        for word in conversation:
            if word in glove_vocab:
                vector += glove_vocab[word]
                count += 1
        if count > 0:
            vector /= count
        embeddings.append(vector)
    return np.array(embeddings)

#OUR DATASET----------------------------------------------------------------------------
#process glove vocab/embeddings for http://nlp.stanford.edu/data/glove.6B.zip:
glove_embeddings_path = '/Users/dishita/Desktop/HumanFac_Data/glove.6B.100d.txt'
glove_vocab = load_glove_vocab(glove_embeddings_path)
print("GloVe vocab loaded!")

# load in our conversations dataset:
df = pd.read_csv("/Users/dishita/Desktop/HumanFac_Data/NoDuplicates_Translated.csv")
print("debug")
df['words'] = df['vectorized_col_1'].apply(preprocess_text)
print("Dataframe loaded!")

#IMPLEMENT GLOVE------------------------------------------------------------------------


# create embeddings for the conversations
df['vectors'] = df['words'].apply(lambda words: create_embeddings([words], glove_vocab)[0])

#RUN KMEANS-----------------------------------------------------------------------

# convert to np array so we can feed it to KMeans 
X = np.array([vec for vec in df['vectors'] if np.isfinite(vec).all()])

#CHANGE HYPERPARAMETER AS NEEDED:
k = 50 
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster_num'] = kmeans.fit_predict(X)
#now each row belongs to a cluster(0-49)
print("KMeans done!")

#PROCESS KMEANS RESULTS--------------------------------------------------------------
#Now we have our clusters, the following functions helps us intrepret the KMeans results --> goal is to 
# get the closet word to each detected centroid 

#for each cluster number, we need to generate a label based on what the cluster is about:
cluster_labels = {}
for i in range(k):
    #if the cluster number matches i, then we want to grab all the words (standalone)
    cluster_labels[i] = df[df['cluster_num'] == i]['words'].explode()

#we want to get the top 10 words from each cluster to call a labe
for cluster in cluster_labels:
    count_of_words = Counter(cluster_labels[cluster])
    top_10 = count_of_words.most_common(10)
    cluster_labels[cluster] = top_10

#now we have a list of words that correspond to each cluster

print("Cluster Labels: ", cluster_labels)
# map cluster number to label
df['cluster_label'] = df['cluster_num'].map(cluster_labels)

# sort by cluster for easy reading
data = df.sort_values(by='cluster_num')

# write output to csv
data.to_csv('clustered_summaries_with_labels.csv', index=False)

