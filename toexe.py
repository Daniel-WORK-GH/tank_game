import subprocess

command = """python -m PyInstaller --noconsole main.py 
--add-data="mapobjects/*;mapobjects/" 
--add-data="maps/*;maps/"
--add-data="menus/*;menus/"
--add-data="network/*;network/"
""".replace('\n', " ")

subprocess.call(command) 