# For installing tools.
# $ make all tidy
#-----------------------------------------------------------------------------------------
.PHONY: all clean tidy
#-----------------------------------------------------------------------------------------
export SNESKIT := $(CURDIR)

# List of binaries to install.
BIN_CA65    := cc65/bin/ca65.exe
BIN_BIN2CA  := bin/bin2ca.py
BIN_PMAGE   := bin/pmage.exe
BIN_SMCONV  := bin/smconv.exe
BIN_SNESBRR := bin/snesbrr.exe
BIN_SNESCHK := bin/sneschk.py

ifneq ($(OS),Windows_NT)
# Strip file extension for Linux.
BIN_CA65    := $(basename $(BIN_CA65))
BIN_BIN2CA  := $(basename $(BIN_BIN2CA))
BIN_PMAGE	:= $(basename $(BIN_PMAGE))
BIN_SMCONV  := $(basename $(BIN_SMCONV))
BIN_SNESBRR := $(basename $(BIN_SNESBRR))
BIN_SNESCHK := $(basename $(BIN_SNESCHK))
endif

ALL_BINS := $(BIN_CA65) $(BIN_BIN2CA) $(BIN_PMAGE) $(BIN_SMCONV) $(BIN_SNESBRR) $(BIN_SNESCHK)

ifeq ($(OS),Windows_NT)
# Add .bat files for each bin/.py file on Windows.
ALL_BINS += $(patsubst %.py,%.bat,$(filter %.py,$(ALL_BINS)))
endif

#-----------------------------------------------------------------------------------------
all: $(ALL_BINS)
	@echo "All set!"

#-----------------------------------------------------------------------------------------
# For Linux, we install ca65 from compiling the source.
# For Windows, we use Python to download the latest binary archive and unzip it.
$(BIN_CA65):
ifneq ($(OS),Windows_NT)
	git clone https://github.com/cc65/cc65.git
	$(MAKE) -C cc65
else
	py windows-install-cc65.py
endif

#-----------------------------------------------------------------------------------------
# Install bin2ca from the tool-src folder.
$(BIN_BIN2CA): tool-src/bin2ca/bin2ca.py
	cp tool-src/bin2ca/bin2ca.py $(BIN_BIN2CA)
ifneq ($(OS),Windows_NT)
	chmod a+x bin/bin2ca
endif

#-----------------------------------------------------------------------------------------
# Install pmage from remote repo source.
$(BIN_PMAGE):
	mkdir -p build
	cd build && git clone https://github.com/mukunda-/pmage
	$(MAKE) -C build/pmage sneskit_install

#-----------------------------------------------------------------------------------------
# Install smconv (snesmod) from remote repo source.
$(BIN_SMCONV):
	mkdir -p build
	cd build && git clone https://github.com/mukunda-/snesmod
	$(MAKE) -C build/snesmod/smconv sneskit_install

#-----------------------------------------------------------------------------------------
# Install snesbrr from remote repo source.
$(BIN_SNESBRR):
	mkdir -p build
	cd build && git clone https://github.com/mukunda-/snesbrr
	$(MAKE) -C build/snesbrr sneskit_install

#-----------------------------------------------------------------------------------------
# Install sneschk from the tool-src folder.
$(BIN_SNESCHK): tool-src/sneschk/sneschk.py
	cp tool-src/sneschk/sneschk.py $(BIN_SNESCHK)
ifneq ($(OS),Windows_NT)
	chmod a+x bin/sneschk
endif

#-----------------------------------------------------------------------------------------
# For Windows, we create bat files to run the python scripts. At the Windows command line,
# you can exclude the extension while calling bat files. So for example, "sneschk" will
# run "sneschk.bat" which will execute sneschk.py with the Windows py launcher.
bin/%.bat: bin/%.py

	echo "@py %SNESKIT%/bin/$*.py %*" > bin/$*.bat

#-----------------------------------------------------------------------------------------
# Remove everything generated.
clean: tidy
	@echo Cleaning up.
	rm -rf cc65
	rm -f bin/*

#-----------------------------------------------------------------------------------------
# Remove intermediate files.
tidy:
	@echo Tidying up.
	rm -rf build
