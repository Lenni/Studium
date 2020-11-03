#ifndef AST
#define AST

#include <fstream>
#include <vector>
#include <list>

class symbol;

#define UNDEFINED_ASTV                          1000
#define SEQUENCE_OF_STATEMENTS_ASTV             1001
#define INCR_ASSIGNMENT_ASTV                    1002
#define DECR_ASSIGNMENT_ASTV                    1003
#define IF_STATEMENT_ASTV                       1004
#define WHILE_STATEMENT_ASTV                    1005
#define VARIABLE_ASTV                           1006
#define CONSTANT_ASTV                           1007
#define CONDITION_LT_ASTV                       1008
#define CONDITION_NLT_ASTV                      1009
#define CONDITION_EQ_ASTV                       1010
#define CONDITION_NEQ_ASTV                      1011
#define CONDITION_GT_ASTV                       1012
#define CONDITION_NGT_ASTV                      1013
#define CONDITION_EM_ASTV                       1014
#define CONDITION_NEM_ASTV                      1015
#define CONDITION_AND_ASTV                      1016
#define CONDITION_OR_ASTV                       1017
#define INPUT_ASTV       	                1018
#define OUTPUT_ASTV       	                1019
#define DEKLARATION_ASTV	                1020

using namespace std;

/**   
 ast vertex
 */
class ast_vertex {
public:
/**   
 index
 */
  int idx;
/**   
 ast vertex type
 */
  int type;
/**   
  address or data
 */
  int adoda;
/**
 * type to string
 */
  string type_to_string();
/** 
 parent
 */
  ast_vertex* parent;
/** 
 children
 */
  list<ast_vertex*> children;

  ast_vertex() : type(UNDEFINED_ASTV), parent(0) {
    static int i=0; idx=i++;
  }
  virtual ~ast_vertex() {
    list<ast_vertex*>::iterator i;
    for (i=children.begin();i!=children.end();i++) delete *i;
  }

  /** 
   print DOT-file
   */
  void draw(ofstream&);

  /** 
   Interpreter
   */
  int interpret();

};

#define YYSTYPE ast_vertex*

/**   
 ast 
 */
class ast {
public:
/**   
 unique root
 */
  ast_vertex* root;
  ast() : root(0) {};
  ~ast() { if (root) delete root; }

/** 
 print DOT-file
 */
  void draw();
};

#endif
