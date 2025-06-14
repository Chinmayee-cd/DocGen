from git import Repo  # pip install GitPython
import time

# Clone the repository if it doesn't exist locally
def clone_repo(repo_url,local_dir):
    try:
        Repo.clone_from(repo_url, local_dir)
        print(f'Repo cloned to {local_dir}')
    except Exception as e:
        print(f'Error cloning repo: {e}')

#Updating repo
def update_repo(repo_url,local_dir):
    repo=Repo(local_dir)
    origin=repo.remotes.origin
    origin.pull()
    print("Repository updated")

#Monitoring for new commits or changes
def monitor_repo(local_dir,interval=60):
    repo=Repo(local_dir)
    origin=repo.remotes.origin
    while True:
        origin.fetch()
        local_commit=repo.head.commit.hexsha
        remote_commit=repo.git.rev_parse('origin/main')
        if local_commit!=remote_commit:
            print("New commits detected! Updating repository...")
            origin.pull()
        else:
            print("No new commits")
        time.sleep(interval)