#!/usr/bin/env python3
#*****************************************************************************************
# sneschk
# (C) 2025 Mukunda Johnson (me@mukunda.com)
# License: MIT
#*****************************************************************************************
import argparse
import os

OUTPUT_FILE = None

#-----------------------------------------------------------------------------------------
def mprint(*args, **kwargs):
   if OUTPUT_FILE is not None:
      print(*args, file=OUTPUT_FILE, **kwargs)
   else:
      print(*args, **kwargs)

#-----------------------------------------------------------------------------------------
def compute_romsize(filesize):
   size_header = 0
   actualsize = 1024
   while actualsize < filesize:
      size_header += 1
      actualsize *= 2
   return size_header, actualsize

#-----------------------------------------------------------------------------------------
def calc_checksum(file, header_start):
   file.seek(0, os.SEEK_SET)
   checksum_addr = header_start + 0xDC
   
   checksum = 0xFF * 2 # Default checksum bytes at 7FDC and 7FDD
   address = 0
   while True:
      c = file.read(4096)
      if c == b'':
         break
      
      checksum += sum(c)
      relative_ffdc = checksum_addr - address
      if relative_ffdc >= 0 and relative_ffdc < len(c):
         # This block contains the checksum bytes. Exclude them from the result.
         checksum -= sum(c[checksum_addr - address:checksum_addr - address + 4])
      
      address += len(c)
      
   return checksum & 0xFFFF

#-----------------------------------------------------------------------------------------
def pad_file(file, size):
   file.seek(0, os.SEEK_END)
   
   filesize = file.tell()
   padding = size - filesize
   mprint(f"Writing {padding} bytes of zero-padding.")

   while padding > 1024:
      file.write(b'\x00' * 1024)
      padding -= 1024
   
   if padding > 0:
      file.write(b'\x00' * padding)

#-----------------------------------------------------------------------------------------
def get_file_byte(file, address):
   file.seek(address, os.SEEK_SET)
   return file.read(1)[0]

#-----------------------------------------------------------------------------------------
def validate_sfc(file, minsize):
   file.seek(0, os.SEEK_END)
   if file.tell() < minsize: # Double on hirom.
      return "file is too small to contain a valid cartridge header."
   
   # Kind of hard to find any special signature to verify.

#-----------------------------------------------------------------------------------------
def format_checksum_bytes(checksum_bytes):
   return " ".join([f"{b:02X}" for b in checksum_bytes])

#-----------------------------------------------------------------------------------------
def main(args=None, output_file=None):
   global OUTPUT_FILE
   OUTPUT_FILE = output_file

   parser = argparse.ArgumentParser(
      'sneschk',
      description="""SNES cartridge checksum calculator.

This tool sets the cartridge checksum and size and pads the
file to a power of 2.

For complex cartridges with multiple storage chips, you may
need a different tool. Or you could put in a PR to support
ROM chip specifications. :)
""")

   parser.add_argument('path', help='Path to SFC or SMC file. Must be headerless.')
   parser.add_argument("-m", "--mode", required=True, choices=['lorom', 'hirom'], help='Cartridge mode')
   parser.add_argument("--fix", action="store_true", help='Make changes to the given file. Otherwise, just print info about it.')
   parser.add_argument("-q", "--quiet", action='store_true', help='Suppress output.')
   args = parser.parse_args(args=args)

   mode = "rb"
   if args.fix:
      mode = "r+b"

   header_start = 0x7F00
   min_size = 0x8000
   if args.mode == "hirom":
      header_start = 0xFF00
      min_size = 0x10000

   with open(args.path, mode) as f:
      f.seek(0, os.SEEK_END)
      mprint(f"File size: {f.tell()} bytes")

      validation_error = validate_sfc(f, min_size)
      if validation_error:
         mprint(f"Validation error: {validation_error}")
         mprint("Does this file have an SMC header? Those are not supported.")
         return

      size_header, full_size = compute_romsize(f.tell())
      mprint(f"Computed size header value: {size_header}")
      f.seek(header_start + 0xD7, os.SEEK_SET)
      mprint(f"Current size header value: {f.read(1)[0]}")
      mprint(f"Full size: {full_size//1024} KiB")

      if args.fix:
         pad_file(f, full_size)
         f.seek(header_start + 0xD7, os.SEEK_SET)
         f.write(bytes([size_header]))

      f.seek(header_start + 0xDC, os.SEEK_SET)
      current_checksum_bytes = f.read(4)
      mprint(f"Current checksum bytes: {format_checksum_bytes(current_checksum_bytes)}")

      checksum = calc_checksum(f, header_start)
      xchecksum = checksum ^ 0xFFFF
      checksum_bytes = bytes([xchecksum & 0xFF, xchecksum >> 8, checksum & 0xFF, checksum >> 8])
      mprint(f"Computed checksum bytes: {format_checksum_bytes(checksum_bytes)}")

      if args.fix:
         f.seek(header_start + 0xDC, os.SEEK_SET)
         f.write(checksum_bytes)

if __name__ == "__main__":
   main()