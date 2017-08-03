ASSEMBLER6502	= acme
AS_FLAGS	= -v0 -Wtype-mismatch
RM		= rm

PROGS		= game.prg example.prg
SRCS		= mca2.a output.a charset.a engine.a tail.a

all: $(PROGS)

game.prg: $(SRCS) _game.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) --outfile game.prg --format cbm _game.tmp.a $(SRCS)

example.prg: $(SRCS) _example.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) --outfile example.prg --format cbm _example.tmp.a $(SRCS)

_game.tmp.a: conv.py game.py
	./conv.py game.py > _game.tmp.a

_example.tmp.a: conv.py example.py
	./conv.py example.py > _example.tmp.a

vice: game.prg
	x64 -device8 1 game.prg

clean:
	-$(RM) -f *.o *.tmp $(PROGS) *~ core
