#!/usr/bin/env python3
#***********************************************************
# Configure environment
import venv, os, shutil

venv.create(".venv", with_pip=True)
if os.name == "nt":
   os.system(".venv\\Scripts\\activate")
elif os.name == "posix":
   os.system("source .venv/bin/activate")

os.system("pip install -r requirements.txt")
#***********************************************************

import os, requests, urllib.request, zipfile

#-----------------------------------------------------------------------------------------
def run(command):
   print("Running command: " + command)
   if os.system(command) != 0:
      print("Error running command: " + command)
      exit(1)

#-----------------------------------------------------------------------------------------
def install_cc65():
   if os.name == 'nt':
      # Windows
      # Download from sourceforge
      urllib.request.urlretrieve("https://downloads.sourceforge.net/project/cc65/cc65-snapshot-win64.zip", "cc65/cc65-snapshot-win64.zip")
      with zipfile.ZipFile("cc65/cc65-snapshot-win64.zip", 'r') as zip_ref:
         zip_ref.extractall("cc65")
         
   elif os.name == "posix":
      # Linux
      run("git clone https://github.com/cc65/cc65.git")
      os.chdir("cc65")
      run("make")
      os.chdir("..")
   else:
      print("install_cc65: Unsupported operating system.")

#-----------------------------------------------------------------------------------------
def install_tools():
   if os.name == "posix":
      shutil.copy("tool-src/sneschk/sneschk.py", "tools/sneschk")
      os.chmod("tools/sneschk", 0o755)
   else:
      shutil.copy("tool-src/sneschk/sneschk.py", "tools/sneschk.py")
      # Windows will use the corresponding .bat file to call the py file.
   
#-----------------------------------------------------------------------------------------
install_cc65()
install_tools()