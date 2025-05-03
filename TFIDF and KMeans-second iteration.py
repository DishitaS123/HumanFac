import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

data = pd.read_csv('EDIT_HERE/relevant_rows_summarized.cs') 
#This was run on the second dataset of 381 conversations, which allowed us to identify best practices for
# our codebook

#PRE-PROCESS DATA----------------------------------------------------------------
#this time use a tfidf vectorizer instead of glove 
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['summary'])

#RUN KMEANS----------------------------------------------------------------------
#CHANGE HYPERPARAMETER AS NEEDED:
k = 9 
model = KMeans(n_clusters=k, random_state=42)
model.fit(X)

#PROCESS KMEANS RESULTS----------------------------------------------------------
#Now we have our clusters, the following functions helps us intrepret the KMeans results --> goal is to 
# get the closet word to each detected centroid 
# assign clusters
data['cluster'] = model.labels_

terms = vectorizer.get_feature_names_out()
order_centroids = model.cluster_centers_.argsort()[:, ::-1]

# create cluster labels based on top terms
cluster_labels = {}
for i in range(k):
    top_terms = [terms[ind] for ind in order_centroids[i, :5]]  # top 5 terms
    cluster_labels[i] = ", ".join(top_terms)

# map cluster number to label
data['cluster_label'] = data['cluster'].map(cluster_labels)

# sort by cluster for easy reading
data = data.sort_values(by='cluster')

# write output to csv
data.to_csv('clustered_summaries_with_labels.csv', index=False)
