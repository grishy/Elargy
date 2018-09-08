// mygenerator.js
var Parser = require("jison").Parser;

// a grammar in JSON
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
          ["e + e",  "$$ = $1+$3"],
          ["e - e",  "$$ = $1-$3"],
          ["e * e",  "$$ = $1*$3"],
          ["e / e",  "$$ = $1/$3"],
          ["e ^ e",  "$$ = Math.pow($1, $3)"],
          ["e !",    "$$ = (function(n) {if(n==0) return 1; return arguments.callee(n-1) * n})($1)"],
          ["e %",    "$$ = $1/100"],
          ["- e",    "$$ = -$2", {"prec": "UMINUS"}],
          ["( e )",  "$$ = $2"],
          ["NUMBER", "$$ = Number(yytext)"],
          ["E",      "$$ = Math.E"],
          ["PI",     "$$ = Math.PI"]
       ]
    }
 };

// `grammar` can also be a string that uses jison's grammar format
var parser = new Parser(grammar);

// generate source, ready to be written to disk
var parserSource = parser.generate();

// you can also use the parser directly from memory

// returns true
var t = parser.parse("1+2*2");

console.log(t);

// throws lexical error
// parser.parse("adfe34bc zxg");