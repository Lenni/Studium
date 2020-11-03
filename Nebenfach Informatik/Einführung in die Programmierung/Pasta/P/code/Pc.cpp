#include <stdio.h>

extern void lexinit(FILE*);
extern int yyparse();

bool interactive;

int main(int argc, char* argv[]) {
  interactive=true;
  if (argc>1) {
    FILE *source_file = fopen(argv[1],"r");
    lexinit(source_file);
    interactive=false;
    printf("+++ PROGRAM +++\n\n");
  }
  yyparse();
  return 0;
}
