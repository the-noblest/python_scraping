import pandas as pd

from os import listdir, path


RESULT_FILE = 'result.csv'

csv_files = list(filter(lambda x: '.csv' in x and x != RESULT_FILE, listdir('data')))

df_from_each_file = (pd.read_csv(path.join('data', file), sep=';') for file in csv_files)
df_merged = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv(path.join('data', RESULT_FILE), sep=';', index=False)
