#include <iostream>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <assert.h>
#include "ast.hpp"

using namespace std;

extern int *teller, anzahl_teller;

string ast_vertex::type_to_string() {
  switch (type) {
    case UNDEFINED_ASTV: { return "undef"; }
    case SEQUENCE_OF_STATEMENTS_ASTV: { return "seq"; }
    case DEKLARATION_ASTV: { return "decl"; }
    case IF_STATEMENT_ASTV: { return "if"; }
    case WHILE_STATEMENT_ASTV: { return "while"; }
    case CONDITION_LT_ASTV: { return "<"; }
    case CONDITION_NLT_ASTV: { return ">="; }
    case CONDITION_GT_ASTV: { return ">"; }
    case CONDITION_NGT_ASTV: { return "<="; }
    case CONDITION_EQ_ASTV: { return "=="; }
    case CONDITION_NEQ_ASTV: { return "!="; }
    case CONDITION_EM_ASTV: { return "leer"; }
    case CONDITION_NEM_ASTV: { return "!leer"; }
    case CONDITION_AND_ASTV: { return "&&"; }
    case CONDITION_OR_ASTV: { return "||"; }
    case INCR_ASSIGNMENT_ASTV: { return "+="; }
    case DECR_ASSIGNMENT_ASTV: { return "-="; }
    case VARIABLE_ASTV: { return "var"; }
    case CONSTANT_ASTV: { return "const"; }
    case OUTPUT_ASTV: { return "out"; }
    case INPUT_ASTV: { return "in"; }
    default: { return "bla"; }
  }
}

void ast_vertex::draw(ofstream& dotfile) {
  if (!this) return;
  list<ast_vertex*>::iterator it;
  dotfile << idx << "[label=\"" << idx << " (" << type_to_string();
  dotfile << ")\"]" << endl;
  for (it=children.begin();it!=children.end();it++) {
    (*it)->draw(dotfile);
    if (*it) dotfile << idx << " -> " << (*it)->idx << endl;
  }
}

int ast_vertex::interpret() {
  switch (type) {
    case UNDEFINED_ASTV: { assert(false);; }
    case SEQUENCE_OF_STATEMENTS_ASTV: { 
      list<ast_vertex*>::iterator it;
      for (it=children.begin();it!=children.end();it++) 
        (*it)->interpret();
      break;
    }
    case IF_STATEMENT_ASTV: { 
      if ((*(children.begin()))->interpret()) (*(++(children.begin())))->interpret();
      break;
    }
    case WHILE_STATEMENT_ASTV: { 
      while ((*(children.begin()))->interpret()) (*(++(children.begin())))->interpret();
      break;
    }
    case CONDITION_LT_ASTV: { 
      return (*(children.begin()))->interpret()<(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_NLT_ASTV: { 
      return (*(children.begin()))->interpret()>=(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_GT_ASTV: { 
      return (*(children.begin()))->interpret()>(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_NGT_ASTV: { 
      return (*(children.begin()))->interpret()<=(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_EQ_ASTV: { 
      return (*(children.begin()))->interpret()==(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_NEQ_ASTV: { 
      return (*(children.begin()))->interpret()!=(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_AND_ASTV: { 
      return (*(children.begin()))->interpret()&&(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_OR_ASTV: { 
      return (*(children.begin()))->interpret()||(*(++(children.begin())))->interpret(); 
    }
    case CONDITION_EM_ASTV: { 
      return teller[(*(children.begin()))->adoda]==0; 
    }
    case CONDITION_NEM_ASTV: { 
      return teller[(*(children.begin()))->adoda]!=0; 
    }
    case INCR_ASSIGNMENT_ASTV: { 
      if ((*(children.begin()))->adoda<1||(*(children.begin()))->adoda>anzahl_teller) 
        cout << ":\nSoviele Teller habe ich nicht!" << endl;
      else 
        teller[(*(children.begin()))->adoda]+=(*(++(children.begin())))->interpret();
      return 0;
    }
    case DECR_ASSIGNMENT_ASTV: { 
      if ((*(children.begin()))->adoda<1||(*(children.begin()))->adoda>anzahl_teller) 
        cout << ":\nSoviele Teller habe ich nicht!" << endl;
      else {
        int i=(*(++(children.begin())))->interpret();
        if (teller[(*(children.begin()))->adoda]<i)
          cout << ":\nEs liegen nicht genug Nudeln auf Teller " << (*(children.begin()))->adoda << "!" << endl;
        else 
          teller[(*(children.begin()))->adoda]-=(*(++(children.begin())))->interpret();
      }
      break;
    }
    case VARIABLE_ASTV: { 
      return teller[adoda]; 
    }
    case CONSTANT_ASTV: { 
      return adoda; 
    }
    case OUTPUT_ASTV: { 
      int n=(*(children.begin()))->interpret();
      if ((*(children.begin()))->type==CONDITION_LT_ASTV||
          (*(children.begin()))->type==CONDITION_EQ_ASTV||
          (*(children.begin()))->type==CONDITION_GT_ASTV||
          (*(children.begin()))->type==CONDITION_NEQ_ASTV) {
        if (n)
          cout  << ":\nJa." << endl; 
        else
          cout  << ":\nNein." << endl; 
      }
      else {
        cout << ":\nAuf Teller " << (*(children.begin()))->adoda;
        if (n==1) 
          cout  << " liegt " << n << " Nudel." << endl; 
        else
          cout  << " liegen " << n << " Nudeln." << endl; 
      }
      return 0; 
    }
    case INPUT_ASTV: { 
      cout << ":\nWieviele Nudeln liegen auf Teller " << (*(children.begin()))->adoda << "?" << endl << ":-) "; 
      cin >> teller[(*(children.begin()))->adoda]; return 0; 
    }
    default : break;
  }
}

void ast::draw() {
  ofstream dotfile("ast.dot");
  dotfile << "digraph {" << endl;
  if (root) root->draw(dotfile);
  dotfile << "}" << endl;
}

