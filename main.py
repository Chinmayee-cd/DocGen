from git import Repo
from git_repo import clone_repo,update_repo,monitor_repo
from code_parser import extract_metadata
repo_url = "https://github.com/Chinmayee-cd/Gestify"
local_dir = "dir"


clone_repo(repo_url,local_dir)
update_repo(repo_url,local_dir)
monitor_repo(local_dir,interval=300)

metadata=extract_metadata(local_dir)
print(metadata)