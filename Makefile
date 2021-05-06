CURRDIR=$(shell pwd)
DESTBINDIR=/usr/local/bin
NAME=sya

all: none

none:
	@echo 'nothing to do, just run "make install", or "make uninstall"'

install:
	install -pDm755 ${CURRDIR}/${NAME}.py ${DESTBINDIR}/${NAME}

uninstall:
	rm -i ${DESTBINDIR}/${NAME}

.PHONY: all none install link uninstall
