%{ 
#include <cstdlib>
#include <iostream>
#include "ast.hpp"
#include "parser.tab.h"
%}

leere      	[ \t\n]+
nat		0|[1-9][0-9]*
kommentar       "//"[^\n]*

%%

{leere} 			{ cout << yytext; }
{kommentar} 			{ }
"Hole dir"			{ cout << yytext; return HOLE_DIR; } 
"hole dir"			{ cout << yytext; return hOLE_DIR; } 
"1 Nudel"			{ cout << yytext; return NUDEL; } 
"Teller"			{ cout << yytext; return TELLER; } 
"Nudeln"			{ cout << yytext; return NUDELN; } 
"Nimm"				{ cout << yytext; return NIMM; } 
"nimm"				{ cout << yytext; return nIMM; } 
"von"				{ cout << yytext; return VON; } 
"Lege"				{ cout << yytext; return LEGE; } 
"lege"				{ cout << yytext; return lEGE; } 
"auf"				{ cout << yytext; return AUF; } 
"Sag mir"			{ cout << yytext; return SAG_MIR; } 
"sag mir"			{ cout << yytext; return sAG_MIR; } 
"Frag mich"			{ cout << yytext; return FRAG_MICH; } 
"frag mich"			{ cout << yytext; return fRAG_MICH; } 
"soviele"			{ cout << yytext; return SOVIELE; } 
"wieviele"			{ cout << yytext; return WIEVIELE; } 
"wie"				{ cout << yytext; return WIE; } 
"liegen"			{ cout << yytext; return LIEGEN; } 
"wenn"				{ cout << yytext; return WENN; } 
"solange"			{ cout << yytext; return SOLANGE; } 
"sollen"			{ cout << yytext; return SOLLEN; } 
"leer"				{ cout << yytext; return LEER; } 
"nicht"				{ cout << yytext; return NICHT; } 
"voller als"			{ cout << yytext; return VOLLER_ALS; } 
"leerer als"			{ cout << yytext; return LEERER_ALS; } 
"genauso voll wie"		{ cout << yytext; return GENAUSO_VOLL_WIE; } 
"ist"				{ cout << yytext; return IST; } 
"ob"				{ cout << yytext; return OB; } 
"Mache"				{ cout << yytext; return MACHE; } 
"mache"				{ cout << yytext; return mACHE; } 
"Wiederhole"			{ cout << yytext; return WIEDERHOLE; } 
"wiederhole"			{ cout << yytext; return wIEDERHOLE; } 
"folgendes"			{ cout << yytext; return FOLGENDES; } 
"und"				{ cout << yytext; return UND; } 
"oder"				{ cout << yytext; return ODER; } 
"!"				{ cout << yytext; return ARZ; } 
","				{ cout << yytext; return KOMMA; } 
{nat} 				{ cout << yytext;  
                                  yylval=new ast_vertex(); 
                                  yylval->adoda=atoi(yytext);
                                  return NAT; 
                                }
"Bis bald"			{ cout << yytext; return BIS_BALD; } 
. 				{ cout << "FEHLER: " << yytext << "!!!" << endl;}

%%

void lexinit(FILE *source)
{
  yyin=source;
}

