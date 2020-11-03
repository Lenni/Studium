CC=g++ -O3
CPPC=g++ -O3 

Pc : Pc.cpp ast.o parser.tab.o lex.yy.o
	$(CPPC) $^ -o$@ -lfl

parser.tab.c : parser.y
	bison -g -v --defines=parser.tab.h -o $@ $<

lex.yy.c : scanner.l
	flex $<

%.o: %.c
	$(CC) -c $< -o $@

%.o: %.cpp
	$(CPPC) -c $< -o $@

clean :
	rm -f parser.tab.* lex.yy.* *.o Pc *.ps *.dot *.out parser.output parser.pdf

.PHONY: clean 
