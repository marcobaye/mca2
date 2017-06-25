ASSEMBLER6502	= acme
AS_FLAGS	= -v2 -Wtype-mismatch
RM		= rm

PROGS		= mca.prg
SRCS		= mca.a _autogenerated.a

all: $(PROGS)

mca.prg: $(SRCS)
	$(ASSEMBLER6502) $(AS_FLAGS) --outfile mca.prg --format cbm mca.a

_autogenerated.a: conv.py situations.c
	./conv.py situations.c > _autogenerated.a

clean:
	-$(RM) -f *.o *.tmp $(PROGS) *~ core
