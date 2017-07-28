ASSEMBLER6502	= acme
AS_FLAGS	= -v0 -Wtype-mismatch
RM		= rm

PROGS		= game.prg example.prg
SRCS		= mca2.a engine.a tail.a

all: $(PROGS)

game.prg: $(SRCS) _game.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) --outfile game.prg --format cbm _game.tmp.a mca2.a engine.a tail.a

example.prg: $(SRCS) _example.tmp.a
	$(ASSEMBLER6502) $(AS_FLAGS) --outfile example.prg --format cbm _example.tmp.a mca2.a engine.a tail.a

_game.tmp.a: conv.py game.py
	./conv.py game.py > _game.tmp.a

_example.tmp.a: conv.py example.py
	./conv.py example.py > _example.tmp.a

clean:
	-$(RM) -f *.o *.tmp $(PROGS) *~ core
