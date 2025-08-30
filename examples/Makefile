RM		= rm

PROGS		= aotb64.prg aotb128.prg aotb+4.prg aotbsw.prg example.prg

all: $(PROGS)

aotb64.prg: aotb.txt
	mca2.py --arch c64 --outfile aotb64.prg aotb.txt

aotb128.prg: aotb.txt
	mca2.py --arch c128 --outfile aotb128.prg aotb.txt

aotb+4.prg: aotb.txt
	mca2.py --arch plus4 --outfile aotb+4.prg aotb.txt

aotbsw.prg: aotb.txt
	mca2.py --arch steckschwein --outfile aotbsw.prg aotb.txt

example.prg: example.txt
	mca2.py --arch c64 --outfile example.prg example.txt

x64: aotb64.prg
	x64sc -device8 1 -autostartprgmode 1 aotb64.prg

x128: aotb128.prg
	x128 -device8 1 -autostartprgmode 1 aotb128.prg

xplus4: aotb+4.prg
	xplus4 -device8 1 -autostartprgmode 1 aotb+4.prg

clean:
	-$(RM) -f *.prg *~
