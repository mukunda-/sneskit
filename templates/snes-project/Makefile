# SNES Makefile Template
#
# 2025-01-17
#*****************************************************************************************

.SUFFIXES:
.PHONY: clean

ifeq ($(strip $(SNESKIT)),)
$(error SNESKIT not found, please add SNESKIT=<path to sneskit> to your environment)
endif

SNESTOOLS := $(SNESKIT)/tools
SNESGRIT  := $(SNESTOOLS)/snesgrit
SNESCHK   := $(SNESTOOLS)/sneschk
SMCONV    := $(SNESTOOLS)/smconv
CC65      := $(SNESKIT)/cc65/bin
AS        := $(CC65)/ca65
LD        := $(CC65)/ld65

#-----------------------------------------------------------------------------------------
# TARGET is the name of the output binary, excluding extension.
# BUILD is the directory where object files & intermediate files will be placed.
# SOURCES is a list of directories containing source code.
# INCLUDES is a list of directories containing extra header files.
# GRAPHICS is a list of directories containing image files for conversion.
# AUDIO is a list of directories containing audio files.
# MAPMODE is "lorom" or "hirom", configuring the cartridge type.
# MAPFILE is YES if you want to generate a map file with the output.
#-----------------------------------------------------------------------------------------
TARGET   := $(notdir $(CURDIR))
BUILD    := build
SOURCES  := source
INCLUDES := include
GRAPHICS := graphics
AUDIO    := audio
MAPMODE  := lorom
MAPFILE  := YES

#-----------------------------------------------------------------------------------------
# Bootstrap files
STARTFILES  := snes_init.asm snes_zvars.asm snes_decompress.asm snes_joypad.asm

# Target 65816 CPU, -s = smart mode (tracks usage of rep and sep)
ASFLAGS     := --cpu 65816 -s

# For snesmod (if used), we convert to a soundbank target.
SOUNDBANK   := $(BUILD)/soundbank
SMCONVFLAGS := --soundbank --output $(SOUNDBANK)
SNESCHKFLAGS := --fix

ifeq ($(MAPMODE),hirom)
ASFLAGS     += -D HIROM
SMCONVFLAGS += --hirom
SNESCHKFLAGS += -m hirom
else
SNESCHKFLAGS += -m lorom
endif

# Include paths.
INCLUDE := $(foreach dir,$(INCLUDES),-I $(CURDIR)/$(dir)) \
           -I $(CURDIR)/$(BUILD) \
           -I $(SNESKIT)/include

# Main target (the SFC filename).
OUTPUT := $(BUILD)/$(TARGET)

# Linker memory configuration.
LDFLAGS := -C $(CURDIR)/config.ld

# All sources.
VPATH := $(foreach dir,$(SOURCES),$(CURDIR)/$(dir)) \
         $(foreach dir,$(GRAPHICS),$(CURDIR)/$(dir)) \
         $(foreach dir,$(AUDIO),$(CURDIR)/$(dir)) \
         $(SNESKIT)/source 

# Code files
SFILES   := $(STARTFILES) $(foreach dir,$(SOURCES),$(notdir $(wildcard $(dir)/*.asm)))

# Graphics files (converted to code)
PNGFILES := $(foreach dir,$(GRAPHICS),$(notdir $(wildcard $(dir)/*.png)))

# Audio files for conversion with snesmod.
AUDIOFILES := $(foreach dir,$(AUDIO),$(notdir $(wildcard $(dir)/*.*)))

# If any audio files exist, then link the soundbank.asm code.
ifneq ($(AUDIOFILES),)
SFILES := $(BUILD)/soundbank.asm $(SFILES)
endif

# Gather total output files.
OFILES := $(addprefix $(BUILD)/,$(PNGFILES:.png=.o)) \
          $(addprefix $(BUILD)/,$(SFILES:.asm=.o))

#-----------------------------------------------------------------------------------------
all : $(OUTPUT).sfc

#-----------------------------------------------------------------------------------------
$(BUILD):
	mkdir -p $@

#-----------------------------------------------------------------------------------------
clean:
	@echo Removing build files.
	@rm -fr $(BUILD)

#-----------------------------------------------------------------------------------------
# Main target
$(OUTPUT).sfc : $(OFILES)

#-----------------------------------------------------------------------------------------
# Rule for converting PNG graphics
%.res.asm : %.png %.grit $(BUILD)
	@$(SNESGRIT) $<

#-----------------------------------------------------------------------------------------
# Rule for converting audio files
soundbank.asm : $(SBXML) $(AUDIOFILES)
	@echo Compiling Soundbank ...
	@$(SMCONV) $(SMCONVFLAGS) $^

#-----------------------------------------------------------------------------------------
# Assembly step.
$(BUILD)/%.o : %.asm $(BUILD)
	@echo Assembling :: $<
	@$(AS) $(ASFLAGS) $(INCLUDE) $< -o $@

#-----------------------------------------------------------------------------------------
# Link step - create cartridge binary.
$(BUILD)/%.sfc:
	@echo Linking...
ifeq ($(MAPFILE),YES)
	@$(LD) $(LDFLAGS) $(OFILES) -o $@ -m $(@:.sfc=.map)
else
	@$(LD) $(LDFLAGS) $(OFILES) -o $@
endif

	@echo "Running sneschk (checksums and padding)"
	$(SNESCHK) $(SNESCHKFLAGS) $@ 

	@echo Okay! :: $(notdir $@)
