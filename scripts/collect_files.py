# -*- coding: utf-8 -*-

import requests
from pathlib import Path
import pandas as pd
from numpy import random
from time import sleep
from tqdm import tqdm
# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
from bs4 import UnicodeDammit


BASE_URL = "https://raw.githubusercontent.com/"


def download_file(data_dir: str, repo_url: str, tree: str, filename: str) -> None:
    # split the repositry name from the url
    repo_name: str = repo_url.split('/', maxsplit=3)[-1]

    # create the request url
    request_url = BASE_URL + f"{repo_name}/{tree}/{filename}"

    try:
        response = requests.get(request_url)

        if not response.ok:
            raise Exception(f"Problem fetching file: {request_url}")

        # create the directory for the repository if it doesn't exist
        # replace the / in the repo name with _&_ to prevent subdirectories
        # example for repo name "IBM/AIX360" --> output dir will be "IBM_&_AIX360"
        output_dir = Path(data_dir, repo_name.replace('/', '_&_'))
        output_dir.mkdir(parents=True, exist_ok=True)

        # create the output file to save the test file into
        # replace the / in the filename with _&_ to prevent subdirectories
        # example for filename "tests/test_camera.py" --> output file will be "tests_&_test_camera.py"
        output_file = Path(output_dir, filename.replace('/', '_&_'))
        output_file.touch()
        output_file.write_text(UnicodeDammit(response.text).unicode_markup)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    except Exception as e:
        with open(Path(data_dir, "errors.txt").resolve(), 'a') as f:
            f.write(f"{repo_url}/tree/{tree}/{filename}\n")


    return


if __name__ == "__main__":
    data_folder: Path = Path("..", "data", "python_flaky_tests")
    data_file: Path = Path.joinpath(data_folder, "active_repos.csv")
    df = pd.read_csv(data_file, usecols=[1, 2, 3, 4])
    df.drop_duplicates(inplace=True)
    repos_dir = Path("..", "data", "repos")

    pbar = tqdm(df[:--000].iterrows())

    for index, row in pbar:
        pbar.set_description(f"project: {row['Project_Name']}  File: {row['Test_filename']}")

        sleep(random.uniform(0, 2))
        download_file(data_dir=repos_dir, repo_url=row['Project_URL'],
                      tree=row['Project_Hash'], filename=row['Test_filename'])
