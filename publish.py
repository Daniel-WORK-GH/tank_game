import subprocess

gitadd = "git add *"
gitcommit = f"""git commit --all -m"{input("Commit message: ")}" """
gitpush = "git push"

subprocess.call(gitadd)
subprocess.call(gitcommit)
subprocess.call(gitpush)