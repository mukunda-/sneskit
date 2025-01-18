## sneschk

This is a tool to fix up a compiled SNES ROM. It pads the size to a power of 2 and
updates the checksum.

Some cartridges contain multiple ROM chips and can have non-power-of-two sizes which
complicates the checksum process. That is not supported (yet?).

### Basic usage
```
sneschk mygame.sfc --fix
```

* Pads the binary and updates the checksum and ROM size header fields.