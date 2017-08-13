ASSEMBLER6502	= acme
AS_FLAGS	= -v0 -Wtype-mismatch
RM		= rm

PROGS		= game64.prg game128.prg example.prg
SRCS		= mca2.a output.a charset.a engine.a tail.a

all: $(PROGS)

game64.prg: $(SRCS) _game.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) -DISO=1 -DSYSTEM=64 --outfile game64.prg --format cbm _game.tmp.a $(SRCS)
	#exomizer sfx basic game64.prg sfx.prg

game128.prg: $(SRCS) _game.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) -DISO=1 -DSYSTEM=128 --outfile game128.prg --format cbm _game.tmp.a $(SRCS)

example.prg: $(SRCS) _example.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) -DISO=0 -DSYSTEM=64 --outfile example.prg --format cbm _example.tmp.a $(SRCS)

_game.tmp.a: conv.py game.py
	./conv.py game.py > _game.tmp.a

_example.tmp.a: conv.py example.py
	./conv.py example.py > _example.tmp.a

x64: game64.prg
	x64 -device8 1 -autostartprgmode 1 game64.prg

x128: game128.prg
	x128 -device8 1 -autostartprgmode 1 game128.prg

clean:
	-$(RM) -f *.o *.tmp $(PROGS) *~ core
