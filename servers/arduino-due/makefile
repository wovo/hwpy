#============================================================================
#
# simple project makefile (just a main file)
#
# (c) Wouter van Ooijen (wouter@voti.nl) 2017
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)
#
#============================================================================

# source files in this project (main.* is automatically assumed)
SOURCES :=

# header files in this project
HEADERS := ../commands.hpp

# other places to look for files for this project
SEARCH  :=

# settings for Arduino Due projects
TARGET            ?= arduino_due
#SERIAL_PORT       ?= COM3
CONSOLE_BAUDRATE  ?= 115200

# include the hwlib makefile, which includes rtos and bmptk
RELATIVE          ?= ./../../..
TI-SOFTWARE       ?= $(RELATIVE)
HWLIB             ?= $(TI-SOFTWARE)/hwlib
BMPTK             ?= $(TI-SOFTWARE)/bmptk
include           $(HWLIB)/makefile.inc
