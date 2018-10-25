var prsr = new parser();
var parseTree = prsr.parseString(lexer("1 + 500"));
prsr.parseTreeToAST(parseTree);
console.log('============\n',prsr.ast);
prsr.parseTreeToHTML(prsr.parseTree[0]);
prsr.astTreeToHTML(prsr.ast);


