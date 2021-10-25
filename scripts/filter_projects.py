import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    data_folder: Path = Path("../data/python_flaky_tests")
    data_file: Path = Path.joinpath(data_folder, "TestsOverview.csv")
    df = pd.read_csv(data_file, usecols=[0, 1])
    df.drop_duplicates(inplace=True, ignore_index=True)
    print(df.info)

