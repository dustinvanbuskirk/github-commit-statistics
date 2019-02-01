import os
import json
import pandas as pd
from github import Github


# def run_command(full_command):
#     proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     output = proc.communicate()
#     print(output)
#     if proc.returncode != 0:
#         sys.exit(1)
#     return b''.join(output).strip().decode()  # only save stdout into output, ignore stderr

# def pr_merge(github_token):
#     g = Github(github_token)


def main():

    github_token = os.getenv('GITHUB_TOKEN')
    github_org = os.getenv('GITHUB_ORG')

    # PyGitHub Auth

    g = Github(github_token)

    total_commits = []
    
    for repo in g.get_organization(github_org).get_repos():

        current_repo = g.get_repo('/'.join([github_org, repo.name]))

        print('Repository: {}'.format(current_repo.name))

        stats = current_repo.get_stats_commit_activity()

        weekly_totals = []

        for i in stats:
            weekly_totals.append([i.week, i.total])
            total_commits.append([i.week, i.total])

        df = pd.DataFrame(weekly_totals, columns = ['date' , 'value']) 

        df.date = pd.to_datetime(df.date)
        dg = df.groupby(pd.Grouper(key='date', freq='1M')).sum() # groupby each 1 month
        dg.index = dg.index.strftime('%B')

        print(dg)

    print('Total of all Repositories for Organization: {}'.format(github_org))

    df = pd.DataFrame(total_commits, columns = ['date' , 'value']) 

    df.date = pd.to_datetime(df.date)
    dg = df.groupby(pd.Grouper(key='date', freq='1M')).sum() # groupby each 1 month
    dg.index = dg.index.strftime('%B')

    print(dg)

if __name__ == "__main__":
    main()