#!/usr/bin/env python3
#***********************************************************
# Configure environment
import venv, os, shutil, glob

# Set SNESKIT environment variable
if os.environ.get("SNESKIT") is None:
   sneskit_path = os.path.dirname(os.path.abspath(__file__))
   os.environ["SNESKIT"] = sneskit_path
   print(f"SNESKIT environment variable set to: {sneskit_path}")

print("Creating venv.")
venv.create(".venv", with_pip=True)

print("Activating venv.")
if os.name == "nt":
   os.system(".venv\\Scripts\\activate")
elif os.name == "posix":
   os.system("source .venv/bin/activate")

print("Installing Python requirements.")
os.system("pip install -r requirements.txt")

print("Okay, ready for work.")
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
   print("Installing cc65.")
   if glob.glob("cc65/*") != []:
      print("*** cc65 has files in it. Skipping installation.")
      return
   
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
   print("Installing tools.")
   if os.name == "posix":
      # Linux calls the script directly.
      shutil.copy("tool-src/sneschk/sneschk.py", "bin/sneschk")
      os.chmod("bin/sneschk", 0o755)
   else:
      # Windows will use the corresponding .bat file to call the py file.
      shutil.copy("tool-src/sneschk/sneschk.py", "bin/sneschk.py")

#-----------------------------------------------------------------------------------------
def bin_exists(filename):
   if os.name == "posix":
      return os.path.exists(f"bin/{filename}")
   else:
      return os.path.exists(f"bin/{filename}.exe")

#-----------------------------------------------------------------------------------------
def install_snesbrr():
   if bin_exists("snesbrr"):
      print("*** snesbrr already installed. Skipping installation.")
      return
   run("mkdir -p build")
   run("cd build")
   run("git clone https://github.com/mukunda-/snesbrr")
   run("cd snesbrr")
   run("make sneskit_install")
   run("cd ../..")
   
#-----------------------------------------------------------------------------------------
def install_snesmod():
   if bin_exists("smconv"):
      print("*** smconv already installed. Skipping installation.")
   run("mkdir -p build")
   run("cd build")
   run("git clone https://github.com/mukunda-/snesmod")
   run("cd snesmod/smconv")
   run("make sneskit_install")
   run("cd ../..")

#-----------------------------------------------------------------------------------------
install_cc65()
install_tools()
install_snesbrr()
install_snesmod()
