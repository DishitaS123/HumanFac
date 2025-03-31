import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def process_clusters(input_csv, no_duplicates_csv, output_dir, num_clusters, search_words=None):
    if search_words is None:
        search_words = ["vulnerability", "security", "secure", "insecure"]

    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Separate ID column
    ids = df.iloc[:, 0]  # First column is ID
    data = df.iloc[:, 1:]  # The rest are feature columns

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)  # Normalize only feature columns

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(data_scaled)

    # Add cluster labels to the original DataFrame
    df["Cluster"] = clusters

    df_with_clusters = pd.concat([ids, df["Cluster"]], axis=1)
    os.makedirs(output_dir, exist_ok=True)
    df_with_clusters.to_csv(f"{output_dir}/clustered_data.csv", index=False)

    # Load the NoDuplicates_Translated file
    no_duplicates_df = pd.read_csv(no_duplicates_csv)

    # Group by clusters and create separate CSV files
    cluster_output_dir = f"{output_dir}/clusters/k={num_clusters}"
    os.makedirs(cluster_output_dir, exist_ok=True)

    for cluster_id in range(num_clusters):
        cluster_ids = df_with_clusters[df_with_clusters["Cluster"] == cluster_id]["ID"]
        cluster_texts = no_duplicates_df[no_duplicates_df["first_col"].isin(cluster_ids)]
        cluster_texts.to_csv(f"{cluster_output_dir}/cluster{cluster_id}.csv", index=False)

    # Create a dictionary to store word counts for each cluster
    word_counts = {word: [] for word in search_words}

    # Iterate through each cluster file
    for cluster_id in range(num_clusters):
        cluster_file = f"{cluster_output_dir}/cluster{cluster_id}.csv"
        if os.path.exists(cluster_file):
            cluster_df = pd.read_csv(cluster_file)

            # Combine all text into a single string
            combined_text = " ".join(cluster_df.iloc[:, 1].astype(str))  # Assuming text is in the second column

            # Count occurrences of each word
            for word in search_words:
                count = combined_text.lower().count(word)
                word_counts[word].append((cluster_id, count))

    # Write word counts and cluster appearance counts to a results.txt file
    results_file = os.path.join(cluster_output_dir, "results.txt")
    with open(results_file, "w") as f:
        # Write word counts for each cluster
        for word, counts in word_counts.items():
            f.write(f"Word: {word}\n")
            # Sort clusters by count in descending order and take the top 10
            top_clusters = sorted(counts, key=lambda x: x[1], reverse=True)[:10]
            for cluster_id, count in top_clusters:
                f.write(f"  Cluster {cluster_id}: {count} occurrences\n")

        # Count the number of times each cluster appears in the top 10 lists for the search words
        cluster_appearance_counts = {}

        for word, counts in word_counts.items():
            # Sort clusters by count in descending order and take the top 10
            top_clusters = sorted(counts, key=lambda x: x[1], reverse=True)[:10]
            for cluster_id, _ in top_clusters:
                if cluster_id not in cluster_appearance_counts:
                    cluster_appearance_counts[cluster_id] = 0
                cluster_appearance_counts[cluster_id] += 1

        # Sort clusters by appearance count in descending order
        sorted_clusters = sorted(cluster_appearance_counts.items(), key=lambda x: x[1], reverse=True)

        # Write the top 10 clusters by appearance count
        f.write("Top 10 clusters by appearance count:\n")
        for cluster_id, count in sorted_clusters[:10]:
            f.write(f"Cluster {cluster_id}: {count} appearances\n")

        print(f"k={num_clusters}. Top 10 clusters by appearance count:\n")
        for cluster_id, count in sorted_clusters[:10]:
            print(f"Cluster {cluster_id}: {count} appearances")
        

if __name__ == "__main__":
    input_csv = "output_data/encoded_data.csv"
    no_duplicates_csv = "input_data/NoDuplicates_Translated.csv"
    output_dir = "output_data"

    for num_clusters in [10, 100, 1000, 5000]:
        print(f"Processing for k={num_clusters} clusters...")
        process_clusters(input_csv, no_duplicates_csv, output_dir, num_clusters)