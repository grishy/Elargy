var prsr = new parser("1 + 500 - 33");
console.log(prsr);
var parseTree = prsr.parseString(lexer("1 + 500 * 3 + 10 +1 + 2 + 213214 + 21424124"));
prsr.parseTreeToAST(parseTree);
console.log('============\n',prsr.ast);
prsr.astTreeToHTML(prsr.ast);


