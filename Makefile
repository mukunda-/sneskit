# For installing tools.

.PHONY: all

export SNESKIT := $(CURDIR)

#-----------------------------------------------------------------------------------------
all: cc65/bin/ca65 bin/sneschk

#-----------------------------------------------------------------------------------------
cc65/bin/ca65:
	git clone https://github.com/cc65/cc65.git
	cd cc65
	make

#-----------------------------------------------------------------------------------------
# sneschk - from the local repo
bin/sneschk: tool-src/sneschk/sneschk.py
	cp tool-src/sneschk/sneschk.py bin/sneschk
	chmod a+x bin/sneschk

#-----------------------------------------------------------------------------------------
# SNESMOD smconv
bin/smconv:
	mkdir -p build
	cd build
	git clone https://github.com/mukunda-/snesmod
	cd snesmod/smconv
	make sneskit_install

#-----------------------------------------------------------------------------------------
# snesbrr
bin/snesbrr:
	mkdir -p build
	cd build
	git clone https://github.com/mukunda-/snesbrr
	cd snesbrr
	make sneskit_install

#-----------------------------------------------------------------------------------------
bin/bin2ca:
	cp tool-src/bin2ca/bin2ca.py bin/bin2ca
	chmod a+x bin/bin2ca

#-----------------------------------------------------------------------------------------
clean:
	rm -rf cc65
	rm -f bin/sneschk bin/smconv bin/snesbrr bin/bin2ca
