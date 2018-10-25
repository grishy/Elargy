var prsr = new parser();
let inpStr = $("#input-text").val(); 
var parseTree = prsr.parseString(lexer(`1 + 500 * 3 + 10 *1 + 2 * 21 * 214`));
prsr.parseTreeToAST(parseTree);
prsr.astTreeToHTML(prsr.ast);


