"""
This script merges all the test smell csvs in the repos_csvs directory and output a single csv file
"""

import glob
from pathlib import Path
import os
import pandas as pd


csvs_dir = Path('..', 'data', 'repos_csvs')

all_files = glob.glob(os.path.join(csvs_dir, "*.csv"))

all_dfs = (pd.read_csv(f, index_col=None, header=0) for f in all_files)
merged_df = pd.concat(all_dfs, ignore_index=True)

merged_df.to_csv(Path(csvs_dir, 'merged_csvs.csv'))
