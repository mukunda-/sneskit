## SNES Development Kit

`JAN 2025 EDITION`

After checking out the repo, run setup.py to install tools.

Recommended to add SNESKIT to your environment pointing to the SNESKIT folder.

## Tool installations:

### CC65
The cc65 folder is populated with the cc65 compiler. Obtain from cc65.github.io. setup.py
automatically downloads the Windows binaries or compiles for Linux.

The binaries should be at /cc65/bin.

### Additional Documentation
You can add these to your /docs folder:
 * [book1.pdf](http://romhacking.net/docs/226/) - Official SNES programming manual
 * [Programmanual.pdf](www.westerndesigncenter.com/wdc/datasheets/Programmanual.pdf) - If 65816primer.txt isn't enough
 * w65c816s.pdf (missing link) - 65816 datasheet

### Emulators
You can populate your /emu folder with these recommended emulators
 * [ZSNES](www.zsnes.com)
   * A very performant emulator.
 * [Snes9x DEBUG VERSION](https://www.romhacking.net/utilities/241/)
   * Snes9x with additional debug capabilities.
 * [BSNES](https://bsnes.org/)
   * This was up and coming back in the day. Looks to still be updated!
 * [SNESGT](https://www.zophar.net/snes/snesgt.html)
   * Not so sure about this one...

 * [BSNES +DEBUGGER](https://www.romhacking.net/utilities/273/)
   * Not so ure about this one. It's very old.
 
 * ZSNES +DEBUGGER (missing link)
   * Another one I haven't tried.

### Misc
 * [VSNES](http://romhacking.net/utils/274/)
   * SUPER useful for viewing data (like VRAM) in an emulator savestate!
   
 * [SPCTool](http://spcsets.caitsith2.net/spctool/)
   * Very useful for SPC development.

## Getting Started
Two templates are provided in `/template`. One is for LOROM mapping mode, the other is for
HIROM mapping mode. The templates contain a HEADER.ASM which should be modified to suit
your purposes—it contains start vectors, mapping mode, game title, cartridge speed (append
_FAST to map mode to indicate a higher-speed cartridge), and NTSC/PAL can be selected by
changing the region.

## SNESMOD
To use SNESMOD, the SNESMOD source files must be added to the startfiles in the makefile.
see the SNESMOD example.

snesmod.asm sm_spc.asm

## SNESGRIT
This is a graphics converter for SNES which is a modified version of the "GBA Raster Image
Transmogrifier" by Cearn, which is distributed under the GPL. Please contact me
(me@mukunda.com) if you would like to obtain the [modified] source code.

## IRC
Join #snesdev on EFNet!
