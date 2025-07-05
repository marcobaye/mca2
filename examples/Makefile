RM		= rm

PROGS		= aotb-c64.prg aotb-c128.prg aotb-264.prg aotb-sw.prg example.prg

all: $(PROGS)

aotb-c64.prg: aotb.txt
	mca2.py --arch c64 --outfile aotb-c64.prg aotb.txt

aotb-c128.prg: aotb.txt
	mca2.py --arch c128 --outfile aotb-c128.prg aotb.txt

aotb-264.prg: aotb.txt
	mca2.py --arch plus4 --outfile aotb-264.prg aotb.txt

aotb-sw.prg: aotb.txt
	mca2.py --arch steckschwein --outfile aotb-sw.prg aotb.txt

example.prg: example.txt
	mca2.py --arch c64 --outfile example.prg example.txt

x64: aotb-c64.prg
	x64sc -device8 1 -autostartprgmode 1 aotb-c64.prg

x128: aotb-c128.prg
	x128 -device8 1 -autostartprgmode 1 aotb-c128.prg

xplus4: aotb-264.prg
	xplus4 -device8 1 -autostartprgmode 1 aotb-264.prg

clean:
	-$(RM) -f *.prg *~
