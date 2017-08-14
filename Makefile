ASSEMBLER6502	= acme
AS_FLAGS	= -v0 -Wtype-mismatch
RM		= rm

PROGS		= game64.prg game128.prg game264.prg example.prg
SRCS		= mca2.a charset.a engine.a output.a tail.a	# order is important: mca first, tail last, engine before output

all: $(PROGS)

game64.prg: arch64.a _game.tmp.a $(SRCS)
	$(ASSEMBLER6502) $(AS_FLAGS) --format cbm --outfile game64.prg arch64.a _game.tmp.a $(SRCS)
	#exomizer sfx basic game64.prg sfx.prg

game128.prg: arch128.a _game.tmp.a $(SRCS)
	$(ASSEMBLER6502) $(AS_FLAGS) --format cbm --outfile game128.prg arch128.a _game.tmp.a $(SRCS)

game264.prg: arch264.a _game.tmp.a $(SRCS)
	$(ASSEMBLER6502) $(AS_FLAGS) --format cbm --outfile game264.prg arch264.a _game.tmp.a $(SRCS)

example.prg: arch64.a _example.tmp.a $(SRCS)
	$(ASSEMBLER6502) $(AS_FLAGS) --format cbm --outfile example.prg arch64.a _example.tmp.a $(SRCS)

_game.tmp.a: conv.py game.py
	./conv.py game.py > _game.tmp.a

_example.tmp.a: conv.py example.py
	./conv.py example.py > _example.tmp.a

x64: game64.prg
	x64 -device8 1 -autostartprgmode 1 game64.prg

x128: game128.prg
	x128 -device8 1 -autostartprgmode 1 game128.prg

xplus4: game264.prg
	xplus4 -device8 1 -autostartprgmode 1 game264.prg

clean:
	-$(RM) -f *.o *.tmp $(PROGS) *~ core
