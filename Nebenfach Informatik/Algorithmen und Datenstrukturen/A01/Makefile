CPPC=g++
CPPC_ARGS=-Wall -Wextra -pedantic -g
PRGNAME=main

$(PRGNAME): $(PRGNAME).o
	$(CPPC) $(PRGNAME).o -o $(PRGNAME)

$(PRGNAME).o: $(PRGNAME).s
	$(CPPC) -c $(PRGNAME).s

$(PRGNAME).s: $(PRGNAME).cpp
	$(CPPC) -S $(PRGNAME).cpp $(CPPC_ARGS)

clean:
	rm -rf $(PRGNAME).o $(PRGNAME).s $(PRGNAME).cc $(PRGNAME)

run: $(PRGNAME)
	clear
	./$(PRGNAME) $(PRG_ARGS)

.PHONY:	clean run
