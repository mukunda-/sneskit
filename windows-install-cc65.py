#!/usr/bin/env python3
#*****************************************************************************************
# Purpose: Downloads cc65 from sourceforge and unzips it. For Windows environments where
# you aren't sure what commands are available for downloading or unzipping.
import urllib.request, zipfile, os

os.makedirs("cc65", exist_ok=True)
urllib.request.urlretrieve("https://downloads.sourceforge.net/project/cc65/cc65-snapshot-win64.zip", "cc65/cc65-snapshot-win64.zip")
with zipfile.ZipFile("cc65/cc65-snapshot-win64.zip", 'r') as zip_ref:
   zip_ref.extractall("cc65")
