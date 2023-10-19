import subprocess

subprocess.call(["git", "add", "*"])
subprocess.call(["git", "commit", "--all", f"""-m"{input("Commit messege : ")}" """])
subprocess.call(["git", "push"])