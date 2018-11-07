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

function example1(){
    $(".grammar-text").val(`S => A
S => D
A => a b
A => a c
A => A b
D => c D
D => b`);
    $(".terminals-text").val(`a|b|c`);
    $("#input-text").val(`a b b`);
}

function example2(){
    $(".grammar-text").val(`S=>a A B e
A=>A b c
A=>b
B=>d`);
    $(".terminals-text").val(`a|b|c|d|e`);
    $("#input-text").val(`a b b c d e`);
}

function example3(){
    $(".grammar-text").val(`S => E
E => T PLUS E
E => T
T => F MULT T
T => F
F => INTEGER`);
    $(".terminals-text").val(`INTEGER|PLUS|MULT`);
    $("#input-text").val(`INTEGER PLUS INTEGER MULT INTEGER`);
}