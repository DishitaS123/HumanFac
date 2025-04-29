import json
from collections import Counter

input_file = "Deepseek-Analysis/relevant_rows_languages.json"

IDs = [
'pe27jeJ',
'0CeBwDN',
'GSC090N',
'x7BZWKA',
'UdZco6H',
'thXjtpv',
'PIoukbk',
'ZftWuNK',
'ohvWdO2',
'kLMCnRx',
'DkR7vhW',
'hWp1t1K',
'xBpjWHz',
'RA4TuAU',
'6G0GyQC',
'Fa4nAAQ',
'D2ZY9ON',
'fBqsEuT',
'iSLCIgn',
'yhvUPmo',
'1aiwVCg',
'LsvANtR',
's9uGVUC',
'j0xyD9c',
'oLsJoKi',
'0RDEfFm',
'qQuIfXq',
'59D737L',
'9ikNrRR',
'oyoGSVm',
'w4IC7jE',
'erZdaLj',
'Vxpz0en',
'dA5cCCs',
'KnAehHV',
'vuEKjsN',
'zxDuwfa',
'rqB3zKp',
'eNl5SXp',
'gvqS4zh',
'JMA6NXd',
'ljveOSB',
'TNVhAcg',
'oJG6e3h',
'q5K4ZlI',
'g28jNXO',
'R9ZGr10',
'kUYMK0d',
'VjzpVaI',
'4vL4Luw',
'ToZVxjz',
'zIBeuIK',
'uD9tCRO',
'wHbrqY0',
'Yy4c3wL',
'5i9SUrt',
'8146mQO',
'tB4dsBI',
'xU9aXcv',
'28Mwwk9',
'zmoIFGN',
'OsjDw6F',
'iPtGMPH',
'mIIlRVo',
'GEZP3nA',
'VEwOZAK',
'bHPvihr',
'ocOiY0c',
'BjaXxo3',
'wJQP3WT',
'QcCVugx',
'5c2cnne',
'JHGwlee',
'VxIPnSa',
'3sbRtMX',
'GNGwkBO',
'FM8PsZl',
'CAoIZFP',
'N3jaPtL',
'fw6jkGL',
'M6wWC58',
'l2H7WkG',
'lhGLk28',
'AyzaZwN',
'rUU3d4C',
'ENxhIZX',
'VM9LMNs',
'VXmLZLH',
'od0Rk49',
'fdPEhVM',
'u82La7j',
'D5nqGKz',
'UKkV86J',
'QeBRG14',
'o7RdZBG',
'LXu1hD3',
'jOkTM1X',
'cdmSMhh',
'Vuk7m6q',
'lulsfi0',
'2TxZMsD',
'rL5UToj',
'Ly9dqUp',
'Nf7eXj3',
'Fj3La2P',
'EmygeHl',
'ry6HhVN',
'ATmn6O1',
'GgCjYi3',
'bpygFJk',
'8E7z2zv',
'9JPaLFA',
'sQpUh5u',
'P6KbjWo',
'efcAzKB',
'4BFa6km',
'KkdeLKR',
'jEKdtIB',
'2bdi5Ol',
'GwO8NfG',
'ExUzrhI',
'hmRTT5H',
'cHGMwFQ',
'VHJMfwD',
'Tb5kgVb',
'ybKh14B',
'lyNhiwL',
'u5TEEnN',
'V67xPAu',
'zzUqFPJ',
'Km9Mf8E',
'1YVK3tc',
'K1oXXm5',
'SYJIVs0',
'twHQk0g',
'JJD7FwQ',
'yrC8jJZ',
'qLLtcO4',
'vSFeH6a',
'Hr00pI1',
'DJc2uOd',
'IAqA3CZ',
'vBnS5iA',
'GOwX4qB',
'dY2kSou',
'VZwgCDu',
'aGAAgVq',
'wESCTRj',
'0FMBnwN',
'i0c1RFz',
'nO0RO7c',
'vnznQbR',
'xkMDPvR',
'M4QvxLR',
'09bBkhP',
'4f3w4li',
'1aBgrHV',
'qANwga1',
'AShyWJg',
'4l20WrY',
'qBJowYK',
'5kx3ba6',
'EI2XSsA',
'6hx2YbK',
'WKWLyqV',
'kTsaxCJ',
'2Phyg03',
'UuGlb1T',
'IUYZ2tH',
'IPNctDS',
'EPpaO1E',
'h5fGzTI',
'pKvCkGg',
'bpcULp9',
'cEFR8NE',
'M9HrWdI',
'Kw4PvVX',
'WrL8Wcy',
'xHQQv9k',
'nClxnMg',
'VBrsChN',
'UGi7zQF',
'3aqNmCx',
'YEb4lH7',
'DSDdNLm',
'dPK92qW',
'g3YBx1n',
'yW6WXTU',
'mfi8wDB',
'DMTeX8s',
'bcEnQGw',
'TYGXFkZ',
'Og9h3C1',
'z4xePOa',
'FvPIaX0',
'bgukbDK',
'nt1YN7O',
'zU2dokJ',
'2nlCcmu',
'9W0iexr',
'YkZ6uIx',
'PJ3vs2N',
'OeXYu3F',
'fd0QVDg',
'iojsSPs',
'REEkT8b',
'4hRlgyb',
'oGvKL5W',
'JUHW8eC',
'NZePZdp',
'fwalRhK',
'R8PRW4m',
'HSJi4eb',
'kXxkoAj',
'49ZsIT0',
'ui65DV0',
'kW0OsSS',
'Sd707gV',
'JYKAgJj',
'L6mKGcG',
'9PvLhcV',
'tnm8g4a',
'whQhKxi',
'v11l4OB',
'5oXbX3c',
'AkCujB6',
'My7LAKo',
'9Iny5yg',
'hh8My6E',
'oMqra7E',
'bRIujGr',
'dCS2Bsz',
'lUm5KRX',
'pHkyIEj',
'M3NKeU0',
'DqOywni',
'oRQx8H5',
'WkZlz35',
'QkB1WMS',
'F5VYO7T',
'fR3HNTm',
's3JFhkn',
'H7smj93',
'P41bBlm',
'wNBG8Gp',
'Mzd1BGr',
'hjZP22N',
'cr76tIf',
'CY5FzHn',
'sKoZymY',
'9ojnMMH',
'brVov5R',
'Ilgqjvd',
'kFQ2UX0',
'mn4F0xm',
'7VgyHCq',
'lih8Bud',
'Tioq77q',
'zMOTq4U',
'ueeBhx1',
'b0NNQoa',
'BamqXJo',
'mtQLOGN',
'dowrg0y',
'Bcmcw6i',
'LeIcv2Y',
'BPhweN9',
'yd4tqPc',
'Sq3nXBV',
'MQHhXZY',
'IS3SDoB',
'4DxpUcy',
'MWBWmYn',
'3Qee1K9',
'4k1Tl1q',
'tyzMFVY',
'J7VHVC0',
'FsTuZwG',
'998xJ74',
'kgekZ1A',
'0TePkC1',
'CInujeL',
'29XiwYT',
'p4dld0u',
'QWE8USn',
'yCTA8Be',
'OVmROa2',
'r2CWKoi',
'8k7z1Mq',
'WlIBru8',
'pY1cMu3',
'ga4VqX9',
'vbAvZzL',
'NfIQEzH',
'uHhbXLS',
'Bvp9fUK',
'v58K4M6',
'oQELvU5',
'c1VfpQq',
'mdCXcqd',
'w4ZZpFx',
'paK0utm',
'tw66zRi',
'DBG9iPt',
'5Bg755G',
'8tPVljY',
'4BNzdK5',
'cYovhTA',
'feaLwAe',
'zHkTtNj',
'J57UNKJ',
'QCCkWGA',
'coYqAQp',
'2PrZSDt',
'QALGSx0',
'ShWAooi',
'MdB5rRc',
'ivqSurZ',
'f75rkV7',
'ohkJE54',
'MVy2ZeJ',
'qyjG67l',
'ftnUmmt',
'X4gMUlU',
'sg0biaz',
'opSAAue',
'sMAv3B1',
'BaR2Oa1',
'NMoHUvF',
'gPObPIp',
'ankfvn5',
'0KTQc3J',
'XevfNr5',
'UI1uflj',
'Z5TgSdi',
'0h1KzOq',
'zvy65zQ',
'6uxEmxw'
]

# Convert the list of IDs to a set for faster lookups
id_set = set(IDs)

# Initialize a Counter for languages found for specified IDs
language_counts = Counter()

# Initialize a list for IDs found in the data but NOT in the specified IDs
ids_not_in_list = []

# Initialize a set to track which IDs from id_set were found in the data
found_ids_from_list_in_data = set()


# Load the JSON file using a proper file object and error handling
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {input_file} was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {input_file}. Please check the file format.")
    exit()
except Exception as e: # Catch other potential errors during file processing
     print(f"An unexpected error occurred: {e}")
     exit()

# Iterate through the data once to classify IDs and count languages
for row in data:
    # Assuming the ID key is 'id', adjust if it's 'ID'
    item_id = row.get('id')
    summary = row.get('summary') # Get the summary

    # Check if the item has an ID
    if item_id is not None:
        if item_id in id_set:
            # This ID is in our list, count its summary and mark as found
            found_ids_from_list_in_data.add(item_id)
            if summary is not None: # Only count if summary exists
                language_counts[summary] += 1
        elif item_id not in id_set:
            # This ID is NOT in our list, add it to the other list
            ids_not_in_list.append(item_id)
    # Optional: You could add an 'else' here to handle rows with no 'id' key at all
    # else:
    #     print(f"Warning: Row without a valid 'id' key skipped: {row}")


# Calculate IDs that were in the specified list but NOT found in the data
ids_in_list_but_not_in_data = id_set - found_ids_from_list_in_data # Set difference


# Print results for languages counted within specified IDs that were found
print("--- Language counts for specified IDs (found in data) ---")
total_count_specified_ids_found = 0
# language_counts is already a Counter, iterate directly
for language, count in language_counts.items():
    if language is not None: # language is guaranteed not to be None here by logic
        print(f"{language}: {count}")
        total_count_specified_ids_found += count

print(f"\nTotal conversations for specified IDs (found in data): {total_count_specified_ids_found}")


# Print results for IDs found in the data but NOT in the specified list
print("\n--- IDs found in data but NOT in the specified list ---")
if ids_not_in_list:
    # Optional: sort the list for cleaner output
    ids_not_in_list.sort()
    for item_id in ids_not_in_list:
        print(item_id)
    print(f"\nTotal count of IDs found in data but not in specified list: {len(ids_not_in_list)}")
else:
    print("No IDs found in the data that were not in the specified list.")


# Print results for IDs in the specified list but NOT found in the data
print("\n--- IDs in specified list but NOT found in data ---")
if ids_in_list_but_not_in_data:
    # Convert set to list and sort for cleaner output
    missing_ids_list = sorted(list(ids_in_list_but_not_in_data))
    for item_id in missing_ids_list:
        print(item_id)
    print(f"\nTotal count of IDs in specified list but not found in data: {len(ids_in_list_but_not_in_data)}")
else:
    print("All IDs from the specified list were found in the data.")