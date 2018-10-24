const Specification = {
    // Base
    _SKIP: /(\t|\n)+/,
    // Elargy
    LPAREN: /\(/,
    RPAREN: /\)/,
    INTEGER: /\d+/,
    PLUS: /\+/,
    MULT: /\*/
};

const arrayOfRegex = Object.entries(Specification).map(el => {
    const name = el[0];
    const regex = el[1].source;
    const group = `(?<${name}>${regex})`;
    return group;
});

const TOKEN_REGEX = new RegExp(arrayOfRegex.join("|"), "g");

function lexer(text) {
    let out = [];
    let result;
    while ((result = TOKEN_REGEX.exec(text))) {
        let token;
        let value;
        // Все undefined, кроме одного, надо найти
        for (const key in result.groups) {
            const el = result.groups[key];
            if (el !== undefined) {
                token = key;
                value = el;
                break;
            }
        }
        if (token === "_SKIP") {
            return;
        } else {
            
            /////////////К
            if(token === "PLUS" || token === "MULT"){
                out.push({ token, value, index: result.index, operation: true });
            }    
            /////////////
            else{
                out.push({ token, value, index: result.index });
            }
            
        }
    }
    return out;
}


