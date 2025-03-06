import pandas as pd


csv_file_path = '/Users/nicholaslandry/Desktop/HumanFacProjects/HumanFac/Datasets/Sample_Foreign_Language_Entry.csv'
df = pd.read_csv(csv_file_path)
#print(df.head())

second_element = df.iloc[0, 0]
print(second_element)
