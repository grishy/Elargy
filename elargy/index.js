const lexer = require("./modules/lexer");
const fs = require("fs");

const input = fs.readFileSync("./input/calc1.elg", "utf8");

console.log("Start parsing...");
console.log("--- Lexer ---");

const TOKENS = lexer(input);
fs.writeFileSync("./steps/lexer.json", JSON.stringify(TOKENS, null, 2), "utf8");

console.log("--- LR1 ---");

console.log(TOKENS);
