import json 
import pandas as pd

def from_JSON(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # list to store all filtered conversations with "/code"
    filtered_list = []
    for conversation in data:
        for text in conversation["conversations"]:
            if '/code' in text['value']:
                filtered_list.append(conversation)
                break
    return filtered_list

#call function
file_1 = from_JSON('YOUR FILE PATH/sg_90k_part1.json')
file_2 = from_JSON('YOUR FILE PATH/sg_90k_part2.json')

#concantenate lists 
combined = file_1 + file_2
df = pd.DataFrame(combined)
df.to_csv('Dataframe_Combined_Wrangled.csv', index=False)

print(f"Number of entries: {len(df)}")
