import requests
import subprocess
import pandas as pd
import subprocess

import pandas as pd
from pathlib import Path

CMD_ARGUMENTS = ["git", "ls-remote", "--exit-code", "-h"]


def repo_exists(repo_url: str) -> bool:
    # create the arguments for the git ls-remote command
    cmd = CMD_ARGUMENTS.copy()
    cmd.append(repo_url)

    # run the process silently
    process = subprocess.run(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # if the command doesn't throw an error, the repo exists
    return True if process.returncode == 0 else False


if __name__ == "__main__":
    data_folder: Path = Path("../data/python_flaky_tests")
    data_file: Path = Path.joinpath(data_folder, "TestsOverview.csv")
    df = pd.read_csv(data_file)

    unique_projects = df[["Project_Name", "Project_URL"]].copy()
    unique_projects.drop_duplicates(inplace=True, ignore_index=True)

    results = list()

    # check if repo url exists
    for url in unique_projects.Project_URL.tolist():
        results.append((url, repo_exists(url)))

    results_df = pd.DataFrame(results, columns=["url", "is_active"])
    results_df.to_csv(Path.joinpath(data_folder, "repo_activity_status.csv"))

    # get a list of inactive repos and use it to filter the original data
    inactive_repos = results_df[results_df.is_active == False].url.to_list()
    active_repos_df = df.loc[~df.Project_URL.isin(inactive_repos)]

    # store the filtered results (active repos only)
    active_repos_df.to_csv(Path.joinpath(data_folder, "active_repos.csv"))
