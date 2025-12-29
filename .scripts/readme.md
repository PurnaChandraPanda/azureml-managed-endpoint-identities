## Tips to follow in git
- go to root of repo

- run following script one time
```
gh version
sudo apt update && sudo apt install gh

# optional
sudo apt install --only-upgrade gh 

gh auth login

# set user mail id and user name
git config --global user.email "pupanda@outlook.com" 
git config --global user.name "PurnaChandraPanda"
./.scripts/bootstrap_github_repo.sh
```

- run following script for every check-in
```
./.scripts/git_push.sh "readme update"
```