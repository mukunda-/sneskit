#!/usr/bin/env python3
import os, unittest, sneschk, io

SFC_TMP_FILE = ".testsfc.tmp"

#-----------------------------------------------------------------------------------------
class TestSneschk(unittest.TestCase):

   #--------------------------------------------------------------------------------------
   def call_sneschk(self, args):
      output = io.StringIO()
      sneschk.main(args, output_file=output)
      return output.getvalue()

   #--------------------------------------------------------------------------------------
   def create_sfc_tmp(self, size):
      f = open(SFC_TMP_FILE, "wb")
      while size > 1024:
         f.write(b"\x00" * 1024)
         size -= 1024
      f.write(b"\x00" * size)
      f.seek(0, os.SEEK_END)
      return f

   #--------------------------------------------------------------------------------------
   # Files are padded to powers of 2. This is meant to fix up the raw assembler/linker
   # output which may be an arbitrary file size.
   def test_padding(self):
      with self.create_sfc_tmp(80000) as f: pass
      output = self.call_sneschk([SFC_TMP_FILE])
      self.assertIn("File size: 80000", output)
      self.assertIn("Computed size header value: 7", output)
      self.assertIn("Current size header value: 0", output)
      self.assertIn("Full size: 128 KiB", output)
      self.assertNotIn("bytes of zero-padding", output)
      self.assertEqual(os.path.getsize(SFC_TMP_FILE), 80000)

      output = self.call_sneschk([SFC_TMP_FILE, "--fix"])
      self.assertIn("File size: 80000", output)
      self.assertIn(f"Writing {131072 - 80000} bytes of zero-padding", output)
      self.assertEqual(os.path.getsize(SFC_TMP_FILE), 131072)
      
      with open(SFC_TMP_FILE, "rb") as f:
         f.seek(0xFFD7)
         self.assertEqual(f.read(1)[0], 7)

      os.remove(SFC_TMP_FILE)

   #--------------------------------------------------------------------------------------
   # Invalid ROMs are rejected.
   # There are not many rules to this at all currently - just checking the file size.
   # It's tricky to have a real validation.
   def test_validation(self):
      with self.create_sfc_tmp(0) as f: pass
      output = self.call_sneschk([SFC_TMP_FILE])
      self.assertIn("file is too small to contain a valid cartridge header", output)
      
      with self.create_sfc_tmp(65535) as f: pass
      output = self.call_sneschk([SFC_TMP_FILE])
      self.assertIn("file is too small to contain a valid cartridge header", output)

      with self.create_sfc_tmp(65536) as f: pass
      output = self.call_sneschk([SFC_TMP_FILE])
      self.assertIn("Current checksum bytes: 00 00 00 00", output)

      os.remove(SFC_TMP_FILE)

   #--------------------------------------------------------------------------------------
   def format_byte_string(self, input):
      return " ".join(f"{byte:02X}" for byte in input)

   #--------------------------------------------------------------------------------------
   # The cartridge checksum is computed according to the SNES specs.
   # sneschk updates the file in place.
   # Careful of the "size" header byte which may change from --fix.
   # After --fix, the computed checksum bytes are written back to 0xFFDC-0xFFDF.
   def test_checksum(self):
      with self.create_sfc_tmp(99999) as f:
         f.seek(1, os.SEEK_SET)
         f.write(b"\x01\x02\x03\x04" + b"\xFF" * (266))
         f.seek(0xFFDC, os.SEEK_SET)
         f.write(b"\x11\x11\x11\x11")
         f.seek(0x10000, os.SEEK_SET)
         f.write(b"\x01\x02\x03\x04" * (65536//4))

      # 0xFF*2 is the default checksum complement header
      cs = (1 + 2  + 3 + 4 + 0xFF * 266 + 0xFF*2 + 10 * 16384) & 0xFFFF
      ccs = cs ^ 0xFFFF
      csformatted = self.format_byte_string([ccs & 0xFF, ccs >> 8, cs & 0xFF, cs >> 8])

      output = self.call_sneschk([SFC_TMP_FILE])
      self.assertIn("Current checksum bytes: 11 11 11 11", output)
      self.assertIn(f"Computed checksum bytes: {csformatted}", output)

      output = self.call_sneschk([SFC_TMP_FILE, "--fix"])

      # The extra +7 is the ROM size header byte set by --fix
      cs = (1 + 2  + 3 + 4 + 0xFF * 266 + 0xFF*2 + 7 + 10 * 16384) & 0xFFFF
      ccs = cs ^ 0xFFFF
      csbytes = bytes([ccs & 0xFF, ccs >> 8, cs & 0xFF, cs >> 8])
      csformatted = self.format_byte_string(csbytes)

      self.assertIn("Current checksum bytes: 11 11 11 11", output)
      self.assertIn(f"Computed checksum bytes: {csformatted}", output)

      # Confirm they were written.
      with open(SFC_TMP_FILE, "rb") as f:
         f.seek(0xFFDC)
         self.assertEqual(f.read(4), bytes(csbytes))

      os.remove(SFC_TMP_FILE)

#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
   mydir = os.path.dirname(__file__)
   os.chdir(mydir)
   unittest.main()
