import glob
from pathlib import Path
import os
import pandas as pd


csvs_dir = Path('..', 'data', 'sample_csvs')
all_files = glob.glob(os.path.join(csvs_dir, "*.csv"))

all_dfs = (pd.read_csv(f, index_col=None, header=0) for f in all_files)
merged_df = pd.concat(all_dfs, ignore_index=True)

merged_df.to_csv('delete_me.csv')
print(merged_df)
