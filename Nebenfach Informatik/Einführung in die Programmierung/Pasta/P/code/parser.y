%{

#include<iostream> 
#include"ast.hpp"

#define BUFFER_SIZE 20000

extern int yylex();
extern int yyerror(char*);
extern bool interactive;

int* teller, anzahl_teller;
ast* the_ast_p;
string name;

%}

%token TELLER
%token HOLE_DIR
%token hOLE_DIR
%token NUDELN
%token NUDEL
%token NIMM
%token nIMM
%token VON
%token LEGE
%token lEGE
%token AUF
%token SAG_MIR
%token sAG_MIR
%token FRAG_MICH
%token fRAG_MICH
%token SOVIELE
%token WIEVIELE
%token WIE
%token LIEGEN
%token WENN
%token SOLANGE
%token SOLLEN
%token LEER
%token NICHT
%token MACHE
%token WIEDERHOLE
%token wIEDERHOLE
%token mACHE
%token FOLGENDES
%token VOLLER_ALS
%token LEERER_ALS
%token GENAUSO_VOLL_WIE
%token OB
%token UND
%token ODER
%token IST
%token NAT
%token ARZ
%token KOMMA
%token BIS_BALD

%left ODER
%left UND

%%

programm : 
  {
    teller=0; anzahl_teller=0;
    if (interactive) {
      cout << "Hallo! Wie heisst Du? \n";
      cout << ":-) ";
      cin >> name;
      cout << ":\n";
      cout << "Hallo " << name << "! Was soll ich tun?\n";
      cout << ":-) ";
    }
  } 
    anweisungs_block ARZ BIS_BALD ARZ
  {
    if (interactive) {
      cout << ":\n";
      cout << "Guten Appetit, " << name << "!\n";
    }
    else {
      cout << "\n\n\n+++ DIALOG +++\n";
      $2->interpret();
      cout << ":\n";
      cout << "Guten Appetit!\n";
    }
    the_ast_p=new ast;
    the_ast_p->root=$2;
    the_ast_p->draw();
    delete the_ast_p;  
    return 0;
  }
  ;
deklaration : HOLE_DIR NAT TELLER 
  {
    int* kopie;
    if (teller) {
      kopie=new int[anzahl_teller+1];
      for (int i=0;i<=anzahl_teller;i++) kopie[i]=teller[i];
      delete [] teller;
      teller=new int[anzahl_teller+$2->adoda+1];
      for (int i=0;i<=anzahl_teller;i++) teller[i]=kopie[i];
      for (int i=anzahl_teller+1;i<=anzahl_teller+$2->adoda;i++) teller[i]=0;
      anzahl_teller+=$2->adoda;
      delete [] kopie;
    } 
    else {
      teller=new int[$2->adoda+1];
      for (int i=0;i<=$2->adoda;i++) teller[i]=0;
      anzahl_teller=$2->adoda;
    }
    $$=new ast_vertex();
    $$->type=DEKLARATION_ASTV;
    if (interactive) cout << ":\n:-) ";
  }
  ;
bedingte_deklaration : hOLE_DIR NAT TELLER 
  {
    int* kopie;
    if (teller) {
      kopie=new int[anzahl_teller+1];
      for (int i=0;i<=anzahl_teller;i++) kopie[i]=teller[i];
      delete [] teller;
      teller=new int[anzahl_teller+$2->adoda+1];
      for (int i=0;i<=anzahl_teller;i++) kopie[i]=teller[i];
      for (int i=anzahl_teller+1;i<=anzahl_teller+$2->adoda;i++) teller[i]=0;
      anzahl_teller+=$2->adoda+1;
      delete [] kopie;
    } 
    else {
      teller=new int[$2->adoda+1];
      for (int i=0;i<=$2->adoda;i++) teller[i]=0;
      anzahl_teller=$2->adoda;
    }
    $$=new ast_vertex();
    $$->type=DEKLARATION_ASTV;
  }
  ;
anweisungs_block : anweisung
  {
    $$=new ast_vertex();
    $$->type=SEQUENCE_OF_STATEMENTS_ASTV;
    $$->children.push_back($1);
    $1->parent=$$;
  }
  | anweisungs_block ARZ anweisung
  {
    $$=$1;
    $$->children.push_back($3);
    $3->parent=$$;
  }
  ;
anweisung : lege_auf 
  | nimm_von 
  | sag_mir 
  | frag_mich 
  | wenn_dann 
  | solange 
  | deklaration 
  ;
bedingter_anweisungs_block : bedingte_anweisung 
  {
    $$=new ast_vertex;
    $$->type=SEQUENCE_OF_STATEMENTS_ASTV;
    $$->children.push_back($1);
    $1->parent=$$;
    
  }
  | bedingter_anweisungs_block KOMMA UND bedingte_anweisung
  {
    $$=$1;
    $$->children.push_back($4);
    $4->parent=$$;
  }
  ;
bedingte_anweisung : bedingt_lege_auf 
  | bedingt_nimm_von 
  | bedingt_sag_mir 
  | bedingt_frag_mich 
  | bedingte_deklaration
  | bedingt_wenn_dann
  | bedingt_solange
  ;
lege_auf : LEGE arithmetischer_ausdruck AUF TELLER NAT
  {
    $5->type=VARIABLE_ASTV;
    $$=new ast_vertex();
    $$->type=INCR_ASSIGNMENT_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
    $$->children.push_back($2);
    $2->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  } 
  ;
bedingt_lege_auf : lEGE arithmetischer_ausdruck AUF TELLER NAT
  {
    $5->type=VARIABLE_ASTV;
    $$=new ast_vertex();
    $$->type=INCR_ASSIGNMENT_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
    $$->children.push_back($2);
    $2->parent=$$;
  }
  ;
nimm_von : NIMM arithmetischer_ausdruck VON TELLER NAT
  {
    $5->type=VARIABLE_ASTV;
    $$=new ast_vertex();
    $$->type=DECR_ASSIGNMENT_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
    $$->children.push_back($2);
    $2->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
bedingt_nimm_von : nIMM arithmetischer_ausdruck VON TELLER NAT
  {
    $5->type=VARIABLE_ASTV;
    $$=new ast_vertex();
    $$->type=DECR_ASSIGNMENT_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
    $$->children.push_back($2);
    $2->parent=$$;
  }
  ;
sag_mir : SAG_MIR KOMMA sag_mir_was
  {
    $$=new ast_vertex();
    $$->type=OUTPUT_ASTV;
    $$->children.push_back($3);
    $3->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
bedingt_sag_mir : sAG_MIR KOMMA sag_mir_was
  {
    $$=new ast_vertex();
    $$->type=OUTPUT_ASTV;
    $$->children.push_back($3);
    $3->parent=$$;
  }
  ;
sag_mir_was : WIEVIELE NUDELN AUF TELLER NAT LIEGEN
  {
    $5->type=VARIABLE_ASTV;
    $$=$5;
  }
  | OB bedingung IST
  {
    $$=$2;
  }
  ;
frag_mich : FRAG_MICH KOMMA frag_mich_was
  {
    $$=new ast_vertex();
    $$->type=INPUT_ASTV;
    $$->children.push_back($3);
    $3->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
bedingt_frag_mich : fRAG_MICH KOMMA frag_mich_was 
  {
    $$=new ast_vertex();
    $$->type=INPUT_ASTV;
    $$->children.push_back($3);
    $3->parent=$$;
  }
  ;
frag_mich_was : WIEVIELE NUDELN AUF TELLER NAT LIEGEN SOLLEN
  {
    $5->type=VARIABLE_ASTV;
    $$=$5;
  }
  ;
wenn_dann : MACHE FOLGENDES KOMMA bedingter_anweisungs_block KOMMA WENN bedingung IST
  {
    $$=new ast_vertex();
    $$->type=IF_STATEMENT_ASTV;
    $$->children.push_back($7);
    $7->parent=$$;
    $$->children.push_back($4);
    $4->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
bedingt_wenn_dann : mACHE FOLGENDES KOMMA bedingter_anweisungs_block KOMMA WENN bedingung IST
  {
    $$=new ast_vertex();
    $$->type=IF_STATEMENT_ASTV;
    $$->children.push_back($7);
    $7->parent=$$;
    $$->children.push_back($4);
    $4->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
solange : WIEDERHOLE FOLGENDES KOMMA bedingter_anweisungs_block KOMMA SOLANGE bedingung IST
  {
    $$=new ast_vertex();
    $$->type=WHILE_STATEMENT_ASTV;
    $$->children.push_back($7);
    $7->parent=$$;
    $$->children.push_back($4);
    $4->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
bedingt_solange : wIEDERHOLE FOLGENDES KOMMA bedingter_anweisungs_block KOMMA SOLANGE bedingung IST
  {
    $$=new ast_vertex();
    $$->type=WHILE_STATEMENT_ASTV;
    $$->children.push_back($7);
    $7->parent=$$;
    $$->children.push_back($4);
    $4->parent=$$;
    if (interactive) {
      $$->interpret();
      cout << ":\n:-) ";
    }
  }
  ;
bedingung : TELLER NAT VOLLER_ALS TELLER NAT 
  {
    $$=new ast_vertex;
    $$->type=CONDITION_GT_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
    $5->type=VARIABLE_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
  }
  | TELLER NAT NICHT VOLLER_ALS TELLER NAT 
  {
    $$=new ast_vertex;
    $$->type=CONDITION_NGT_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
    $6->type=VARIABLE_ASTV;
    $$->children.push_back($6);
    $6->parent=$$;
  }
  | TELLER NAT LEERER_ALS TELLER NAT 
  {
    $$=new ast_vertex;
    $$->type=CONDITION_LT_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
    $5->type=VARIABLE_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
  }
  | TELLER NAT NICHT LEERER_ALS TELLER NAT 
  {
    $$=new ast_vertex;
    $$->type=CONDITION_NLT_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
    $6->type=VARIABLE_ASTV;
    $$->children.push_back($6);
    $6->parent=$$;
  }
  | TELLER NAT GENAUSO_VOLL_WIE TELLER NAT 
  {
    $$=new ast_vertex;
    $$->type=CONDITION_EQ_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
    $5->type=VARIABLE_ASTV;
    $$->children.push_back($5);
    $5->parent=$$;
  }
  | TELLER NAT NICHT GENAUSO_VOLL_WIE TELLER NAT 
  {
    $$=new ast_vertex;
    $$->type=CONDITION_NEQ_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
    $6->type=VARIABLE_ASTV;
    $$->children.push_back($6);
    $6->parent=$$;
  }
  | TELLER NAT LEER
  {
    $$=new ast_vertex;
    $$->type=CONDITION_EM_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
  }
  | TELLER NAT NICHT LEER
  {
    $$=new ast_vertex;
    $$->type=CONDITION_NEM_ASTV;
    $2->type=VARIABLE_ASTV;
    $$->children.push_back($2);
    $2->parent=$$;
  }
  | bedingung UND bedingung
  {
    $$=new ast_vertex;
    $$->type=CONDITION_AND_ASTV;
    $$->children.push_back($1);
    $1->parent=$$;
    $$->children.push_back($3);
    $3->parent=$$;
  }
  | bedingung ODER bedingung
  {
    $$=new ast_vertex;
    $$->type=CONDITION_OR_ASTV;
    $$->children.push_back($1);
    $1->parent=$$;
    $$->children.push_back($3);
    $3->parent=$$;
  }
  ;
arithmetischer_ausdruck :  SOVIELE NUDELN KOMMA WIE AUF TELLER NAT LIEGEN KOMMA
  {
    $7->type=VARIABLE_ASTV;
    $$=$7;
  }
  | NUDEL 
  {
    $$=new ast_vertex;
    $$->type=CONSTANT_ASTV;
    $$->adoda=1;
  }
  | NAT NUDELN
  {
    $1->type=CONSTANT_ASTV;
    $$=$1;
  }
  ;

%%

int yyerror(char *msg) { 
  cout << ":\nDas verstehe ich leider nicht! \n"; 
  if (interactive) 
    cout << ":\nBis bald " << name << "!\n"; 
  else
    cout << ":\nBis bald!\n"; 
}
