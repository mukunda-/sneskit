## SNES Development Kit

`JAN 2025 EDITION`

This is an SDK for making SNES games. I would hope that this serves as a useful resource
for SNES adventurers. Note that this is quite a low-level distribution and some of the
tools have been recently updated and may not be stable.

If you're looking for something higher level and potentially easier to work with, you may
want to check out [pvsneslib](https://github.com/alekmaul/pvsneslib/tree/master). This lib
also has much better support for C.

Either way, happy tinkering! Please open an issue if you come across anything confusing or
to suggest improvements. I don't have a lot of personal time to contribute to this, so
other contributions are welcome as well. All of my SNES tools are free to play with and
licensed under MIT.

### Prerequisites:

  * python3 (with pip and venv)
  * git
  * make
  * go

After checking out the repo, run `make all tidy` to install tools. The `bin` folder will
be populated.

SNESKIT should be added to your environment pointing to the sneskit folder.

## Tool installations:

### CC65
The cc65 folder is populated with the cc65 compiler from cc65.github.io.

The binaries should be at /cc65/bin.

### bin2ca
A simple python script to convert binaries to includable assembly files.

### pmage
An SNES-compatible image converter - https://github.com/mukunda-/pmage

The setup makefile will install this from source (Go).

NOTE: This is a rudimentary tool that needs a lot more work to be stable. Contributions
welcome!

### smconv
SNESMOD music converter - https://github.com/mukunda-/snesmod/smconv

The setup makefile will install this from source (Go).

### snesbrr
A tool for converting sound files into compressed brr files (and vice versa) - http://github.com/mukunda-/snesbrr

The setup makefile will install this from source (Go).

### sneschk
A python script to fix the header portion of a compiled cartridge image (SFC).

## Additional Documentation
You can add these to your /docs folder:
 * [Fullsnes](https://problemkaputt.de/fullsnes.htm) - Nocash SNES documentation. Very thorough and detailed.
 * [book1.pdf](http://romhacking.net/docs/226/) - Official SNES programming manual
 * [Programmanual.pdf](www.westerndesigncenter.com/wdc/datasheets/Programmanual.pdf) - If 65816primer.txt isn't enough
 * w65c816s.pdf (missing link) - 65816 datasheet

## Emulators
You can populate your /emu folder with these recommended emulators
 * [Snes9x](https://www.snes9x.com/)
   * A personal favorite.

 * [ZSNES](www.zsnes.com)
   * A very performant emulator.

 * [Snes9x DEBUG VERSION](https://www.romhacking.net/utilities/241/)
   * Snes9x with additional debug capabilities.

 * [BSNES](https://bsnes.org/)
   * This was up and coming as a "super-accurate" emulator back in the day. Looks to still be updated!

 * [SNESGT](https://www.zophar.net/snes/snesgt.html)
   * Not so sure about this one...

 * [BSNES +DEBUGGER](https://www.romhacking.net/utilities/273/)
   * Not so sure about this one. It's very old.
 
 * ZSNES +DEBUGGER (missing link)
   * Another one I haven't tried.

## Other useful resources/tools
 * [VSNES](http://romhacking.net/utils/274/)
   * SUPER useful for viewing data (like VRAM) in an emulator savestate!
   
 * SPCTool (Missing link)
   * Very useful for SPC development.

## Using SNESKIT

### Getting Started
Check `/templates` to get started. Adjust the template files to suit your needs. Common
things you might change are the cartridge memory map (HiROM is much easier to work with),
linker regions, and cartridge header details (NTSC/PAL, title, speed, etc.).

### Syntax Highlighting

 * [VS Code - ca65 Language Support](https://marketplace.visualstudio.com/items?itemName=tlgkccampbell.code-ca65)
   * Extension for VS Code to support ca65.

### snesmod
See example/snesmod for a basic demo. SNESMOD in general could use improvement with
documentation. If you have specific questions, please file an issue and the documentation
can be updated.

### Note about pmage
This is in very early stages and hopefully will evolve over time into a reliable image
conversion tool.

## Contributions welcome!
Check the issues page for things to do.

## IRC
Join #snesdev on EFNet!
