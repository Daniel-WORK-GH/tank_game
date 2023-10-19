import subprocess

gitadd = "git add *"
gitcommit = f"""git commit --all -m"{input("Commit message: ")}" """
gitpush = "git push"

def to_args(str:str):
    return str.strip().split(' ')

subprocess.call(gitadd)
subprocess.call(gitcommit)
subprocess.call(gitpush)