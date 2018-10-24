var prsr = new parser();
var parseTree = prsr.parseString(lexer("1 + 500 * 3 + 10 *1 + 2 * 21 * 214"));
prsr.parseTreeToAST(parseTree);
console.log('============\n',prsr.ast);
prsr.astTreeToHTML(prsr.ast);


