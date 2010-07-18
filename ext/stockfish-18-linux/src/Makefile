# Stockfish, a UCI chess playing engine derived from Glaurung 2.1
# Copyright (C) 2004-2008 Tord Romstad (Glaurung author)
# Copyright (C) 2008-2010 Marco Costalba, Joona Kiiski, Tord Romstad
#
# This file is part of Stockfish.
#
# Stockfish is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stockfish is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


### ==========================================================================
### Section 1. General Configuration
### ==========================================================================

### Executable name
EXE = stockfish

### Installation dir definitions
PREFIX = /usr/local
BINDIR = $(PREFIX)/bin

### Built-in benchmark for pgo-builds
PGOBENCH = ./$(EXE) bench 32 1 10 default depth

### Object files
OBJS = application.o bitboard.o pawns.o material.o endgame.o evaluate.o main.o \
	misc.o move.o movegen.o history.o movepick.o search.o piece.o \
	position.o direction.o tt.o value.o uci.o ucioption.o \
	mersenne.o book.o bitbase.o san.o benchmark.o


### ==========================================================================
### Section 2. High-level Configuration
### ==========================================================================
#
# flag                --- Comp switch --- Description
# ----------------------------------------------------------------------------
#
# debug = no/yes      --- -DNDEBUG    --- Enable/Disable debug mode
# optimize = yes/no   --- (-O3/-fast etc.) --- Enable/Disable optimizations
# arch = (name)       --- (-arch)     --- Target architecture
# os = (name)         ---             --- Target operating system
# bits = 64/32        --- -DIS_64BIT  --- 64-/32-bit operating system
# bigendian = no/yes  --- -DBIGENDIAN --- big/little-endian byte order
# prefetch = no/yes   --- -DUSE_PREFETCH  --- Use prefetch x86 asm-instruction
# bsfq = no/yes       --- -DUSE_BSFQ  --- Use bsfq x86_64 asm-instruction
#                                     --- (Works only with GCC and ICC 64-bit)
# popcnt = no/yes     --- -DUSE_POPCNT --- Use popcnt x86_64 asm-instruction
#
# Note that Makefile is space sensitive, so when adding new architectures
# or modifying existing flags, you have to make sure there are no extra spaces
# at the end of the line for flag values.

### 2.1. General
debug = no
optimize = yes

### 2.2 Architecture specific

# General-section
ifeq ($(ARCH),general-64)
	arch = any
	os = any
	bits = 64
	bigendian = no
	prefetch = no
	bsfq = no
	popcnt = no
endif

ifeq ($(ARCH),general-32)
	arch = any
	os = any
	bits = 32
	bigendian = no
	prefetch = no
	bsfq = no
	popcnt = no
endif

ifeq ($(ARCH),bigendian-64)
	arch = any
	os = any
	bits = 64
	bigendian = yes
	prefetch = no
	bsfq = no
	popcnt = no
endif

ifeq ($(ARCH),bigendian-32)
	arch = any
	os = any
	bits = 32
	bigendian = yes
	prefetch = no
	bsfq = no
	popcnt = no
endif

# x86-section
ifeq ($(ARCH),x86-64)
	arch = x86_64
	os = any
	bits = 64
	bigendian = no
	prefetch = yes
	bsfq = yes
	popcnt = no
endif

ifeq ($(ARCH),x86-64-modern)
	arch = x86_64
	os = any
	bits = 64
	bigendian = no
	prefetch = yes
	bsfq = yes
	popcnt = yes
endif

ifeq ($(ARCH),x86-32)
	arch = i386
	os = any
	bits = 32
	bigendian = no
	prefetch = yes
	bsfq = no
	popcnt = no
endif

ifeq ($(ARCH),x86-32-old)
	arch = i386
	os = any
	bits = 32
	bigendian = no
	prefetch = no
	bsfq = no
	popcnt = no
endif

# osx-section
ifeq ($(ARCH),osx-ppc-64)
	arch = ppc64
	os = osx
	bits = 64
	bigendian = yes
	prefetch = no
	bsfq = no
	popcnt = no
endif

ifeq ($(ARCH),osx-ppc-32)
	arch = ppc
	os = osx
	bits = 32
	bigendian = yes
	prefetch = no
	bsfq = no
	popcnt = no
endif

ifeq ($(ARCH),osx-x86-64)
	arch = x86_64
	os = osx
	bits = 64
	bigendian = no
	prefetch = yes
	bsfq = yes
	popcnt = no
endif

ifeq ($(ARCH),osx-x86-32)
	arch = i386
	os = osx
	bits = 32
	bigendian = no
	prefetch = yes
	bsfq = no
	popcnt = no
endif


### ==========================================================================
### Section 3. Low-level configuration
### ==========================================================================

### 3.1 Selecting compiler (default = gcc)
ifeq ($(COMP),)
	COMP=gcc
endif

ifeq ($(COMP),gcc)
	comp=gcc
	CXX=g++
	profile_prepare = gcc-profile-prepare
	profile_make = gcc-profile-make
	profile_use = gcc-profile-use
	profile_clean = gcc-profile-clean
endif

ifeq ($(COMP),icc)
	comp=icc
	CXX=icpc
	profile_prepare = icc-profile-prepare
	profile_make = icc-profile-make
	profile_use = icc-profile-use
	profile_clean = icc-profile-clean
endif

### 3.2 General compiler settings
CXXFLAGS += -g -Wall -fno-exceptions -fno-rtti $(EXTRACXXFLAGS)

ifeq ($(comp),icc)
	CXXFLAGS += -wd383,869,981,10187,10188,11505,11503
endif

ifeq ($(os),osx)
	CXXFLAGS += -arch $(arch)
endif

### 3.3 General linker settings
LDFLAGS += -lpthread $(EXTRALDFLAGS)

ifeq ($(os),osx)
	LDFLAGS += -arch $(arch)
endif

### 3.4 Debugging
ifeq ($(debug),no)
	CXXFLAGS += -DNDEBUG
endif

### 3.5 Optimization
ifeq ($(optimize),yes)

	ifeq ($(comp),gcc)
		CXXFLAGS += -O3

		ifeq ($(os),osx)
			ifeq ($(arch),i386)
				CXXFLAGS += -mdynamic-no-pic
			endif
			ifeq ($(arch),x86_64)
				CXXFLAGS += -mdynamic-no-pic
			endif
		endif
	endif

	ifeq ($(comp),icc)
		CXXFLAGS += -fast

		ifeq ($(os),osx)
			CXXFLAGS += -mdynamic-no-pic
		endif
	endif
endif

### 3.6. Bits
ifeq ($(bits),64)
	CXXFLAGS += -DIS_64BIT
endif

### 3.7 Endianess
ifeq ($(bigendian),yes)
	CXXFLAGS += -DBIGENDIAN
endif

### 3.8 prefetch
ifeq ($(prefetch),yes)
	CXXFLAGS += -msse
	DEPENDFLAGS += -msse
else
	CXXFLAGS += -DNO_PREFETCH
endif

### 3.9 bsfq
ifeq ($(bsfq),yes)
	CXXFLAGS += -DUSE_BSFQ
endif

### 3.10 popcnt
ifeq ($(popcnt),yes)
	CXXFLAGS += -DUSE_POPCNT
endif

### ==========================================================================
### Section 4. Public targets
### ==========================================================================

default:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) build

help:
	@echo ""
	@echo "To compile stockfish, type: "
	@echo ""
	@echo "make target ARCH=arch [COMP=comp]"
	@echo ""
	@echo "Supported targets:"
	@echo ""
	@echo "build                > Build unoptimized version"
	@echo "profile-build        > Build PGO-optimized version"
	@echo "popcnt-profile-build > Build PGO-optimized version with optional popcnt-support"
	@echo "strip                > Strip executable"
	@echo "install              > Install executable"
	@echo "clean                > Clean up"
	@echo "testrun              > Make sample run"
	@echo ""
	@echo "Supported archs:"
	@echo ""
	@echo "x86-64               > x86 64-bit"
	@echo "x86-64-modern        > x86 64-bit with runtime support for popcnt-instruction"
	@echo "x86-32               > x86 32-bit excluding very old hardware without SSE-support"
	@echo "x86-32-old           > x86 32-bit including also very old hardware"
	@echo "osx-ppc-64           > PPC-Mac OS X 64 bit"
	@echo "osx-ppc-32           > PPC-Mac OS X 32 bit"
	@echo "osx-x86-64           > x86-Mac OS X 64 bit"
	@echo "osx-x86-32           > x86-Mac OS X 32 bit"
	@echo "general-64           > unspecified 64-bit"
	@echo "general-32           > unspecified 32-bit"
	@echo "bigendian-64         > unspecified 64-bit with bigendian byte order"
	@echo "bigendian-32         > unspecified 32-bit with bigendian byte order"
	@echo ""
	@echo "Supported comps:"
	@echo ""
	@echo "gcc                  > Gnu compiler (default)"
	@echo "icc                  > Intel compiler"
	@echo ""
	@echo "Non-standard targets:"
	@echo ""
	@echo "make hpux           >  Compile for HP-UX. Compiler = aCC"
	@echo ""
	@echo "Examples. If you don't know what to do, you likely want to run: "
	@echo ""
	@echo "make profile-build ARCH=x86-64    (This is for 64-bit systems)"
	@echo "make profile-build ARCH=x86-32    (This is for 32-bit systems)"
	@echo ""

build:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) config-sanity
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) all

profile-build:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) config-sanity
	@echo ""
	@echo "Step 0/4. Preparing for profile build."
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_prepare)
	@echo ""
	@echo "Step 1/4. Building executable for benchmark ..."
	@touch *.cpp *.h
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_make)
	@echo ""
	@echo "Step 2/4. Running benchmark for pgo-build ..."
	@$(PGOBENCH) > /dev/null
	@echo ""
	@echo "Step 3/4. Building final executable ..."
	@touch *.cpp
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_use)
	@echo ""
	@echo "Step 4/4. Deleting profile data ..."
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_clean)

popcnt-profile-build:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) config-sanity
	@echo ""
	@echo "Step 0/6. Preparing for profile build."
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_prepare)
	@echo ""
	@echo "Step 1/6. Building executable for benchmark (popcnt disabled)..."
	@touch *.cpp *.h
	$(MAKE) ARCH=x86-64 COMP=$(COMP) $(profile_make)
	@echo ""
	@echo "Step 2/6. Running benchmark for pgo-build (popcnt disabled)..."
	@$(PGOBENCH) > /dev/null
	@echo ""
	@echo "Step 3/6. Building executable for benchmark (popcnt enabled)..."
	@touch *.cpp *.h
	$(MAKE) ARCH=x86-64-modern COMP=$(COMP) $(profile_make)
	@echo ""
	@echo "Step 4/6. Running benchmark for pgo-build (popcnt enabled)..."
	@$(PGOBENCH) > /dev/null
	@echo ""
	@echo "Step 5/6. Building final executable ..."
	@touch *.cpp *.h
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_use)
	@echo ""
	@echo "Step 6/6. Deleting profile data ..."
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) $(profile_clean)
	@echo ""

strip:
	strip $(EXE)

install:
	-mkdir -p -m 755 $(BINDIR)
	-cp $(EXE) $(BINDIR)
	-strip $(BINDIR)/$(EXE)

clean:
	$(RM) $(EXE) *.o .depend *~ core bench.txt

testrun:
	@$(PGOBENCH)

### ==========================================================================
### Section 5. Private targets
### ==========================================================================

all: $(EXE) .depend

config-sanity:
	@echo ""
	@echo "Config:"
	@echo "debug: '$(debug)'"
	@echo "optimize: '$(optimize)'"
	@echo "arch: '$(arch)'"
	@echo "os: '$(os)'"
	@echo "bits: '$(bits)'"
	@echo "bigendian: '$(bigendian)'"
	@echo "prefetch: '$(prefetch)'"
	@echo "bsfq: '$(bsfq)'"
	@echo "popcnt: '$(popcnt)'"
	@echo ""
	@echo "Flags:"
	@echo "CXX: $(CXX)"
	@echo "CXXFLAGS: $(CXXFLAGS)"
	@echo "LDFLAGS: $(LDFLAGS)"
	@echo ""
	@echo "Testing config sanity. If this fails, try 'make help' ..."
	@echo ""
	@test "$(debug)" = "yes" || test "$(debug)" = "no"
	@test "$(optimize)" = "yes" || test "$(optimize)" = "no"
	@test "$(arch)" = "any" || test "$(arch)" = "x86_64" || test "$(arch)" = "i386" || \
	 test "$(arch)" = "ppc64" || test "$(arch)" = "ppc"
	@test "$(os)" = "any" || test "$(os)" = "osx"
	@test "$(bits)" = "32" || test "$(bits)" = "64"
	@test "$(bigendian)" = "yes" || test "$(bigendian)" = "no"
	@test "$(prefetch)" = "yes" || test "$(prefetch)" = "no"
	@test "$(bsfq)" = "yes" || test "$(bsfq)" = "no"
	@test "$(popcnt)" = "yes" || test "$(popcnt)" = "no"
	@test "$(comp)" = "gcc" || test "$(comp)" = "icc"

$(EXE): $(OBJS)
	$(CXX) -o $@ $(OBJS) $(LDFLAGS)

gcc-profile-prepare:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) gcc-profile-clean

gcc-profile-make:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) \
	EXTRACXXFLAGS='-fprofile-generate' \
	EXTRALDFLAGS='-lgcov' \
	all

gcc-profile-use:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) \
	EXTRACXXFLAGS='-fprofile-use' \
	all

gcc-profile-clean:
	@rm -rf *.gcda *.gcno bench.txt

icc-profile-prepare:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) icc-profile-clean
	@mkdir profdir

icc-profile-make:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) \
	EXTRACXXFLAGS='-prof-gen=srcpos -prof_dir ./profdir' \
	all

icc-profile-use:
	$(MAKE) ARCH=$(ARCH) COMP=$(COMP) \
	EXTRACXXFLAGS='-prof_use -prof_dir ./profdir' \
	all

icc-profile-clean:
	@rm -rf profdir bench.txt

.depend:
	-@$(CXX) $(DEPENDFLAGS) -MM $(OBJS:.o=.cpp) > $@ 2> /dev/null

-include .depend


### ==========================================================================
### Section 6. Non-standard targets
### ==========================================================================

hpux:
	$(MAKE) \
	CXX='/opt/aCC/bin/aCC -AA +hpxstd98 -DBIGENDIAN -mt +O3 -DNDEBUG' \
	CXXFLAGS="" \
	LDFLAGS="" \
	all

