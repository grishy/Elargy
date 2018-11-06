// `S => A
// S => D
// A => a b
// A => a c
// A => A b
// D => c D
// D => b`


// `S=>a A B e
// A=>A b c
// A=>b
// B=>d`, `a|b|c|d|e`

//prsr.parseTreeToAST(parseTree);
//prsr.astTreeToHTML(prsr.ast);


function makeParser(){
    var prsr = new parser(String($(".grammar-text").val()),String($(".terminals-text").val()));
    var parseTree = prsr.parseString(prsr.lexer($("#input-text").val().trim()));
    prsr.parseTreeToHTML(prsr.parseTree);
}