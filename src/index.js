var Parser = require("jison").Parser;

var grammar = {
    "lex": {
       "rules": [
          ["\\s+",                    "/* skip whitespace */"],
          ["[0-9]+(?:\\.[0-9]+)?\\b", "return 'NUMBER'"],
          ["\\*",                     "return '*'"],
          ["\\/",                     "return '/'"],
          ["-",                       "return '-'"],
          ["\\+",                     "return '+'"],
          ["\\^",                     "return '^'"],
          ["!",                       "return '!'"],
          ["%",                       "return '%'"],
          ["\\(",                     "return '('"],
          ["\\)",                     "return ')'"],
          ["PI\\b",                   "return 'PI'"],
          ["E\\b",                    "return 'E'"],
          ["$",                       "return 'EOF'"]
       ]
    },
 
    "operators": [
       ["left", "+", "-"],
       ["left", "*", "/"],
       ["left", "^"],
       ["right", "!"],
       ["right", "%"],
       ["left", "UMINUS"]
    ],
 
    "bnf": {
       "expressions": [["e EOF",   "return $1"]],
 
       "e" :[
          ["e + e",  "$$ = [$1, '+',$3]"],
          ["e - e",  "$$ = [$1,'-',$3]"],
          ["e * e",  "$$ = [$1,'*',$3]"],
          ["( e )",  "$$ = ['(',$2,')']"],
          ["NUMBER", "$$ = Number(yytext)"],
       ]
    }
 };

var parser = new Parser(grammar);

var AST = parser.parse("1+2*3");

console.log(AST);