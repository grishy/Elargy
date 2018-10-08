let grammar2 = [
    { leftside: "S", rightside: "A" },
    { leftside: "S", rightside: "D" },
    { leftside: "A", rightside: "a b" },
    { leftside: "A", rightside: "a c" },
    { leftside: "A", rightside: "A b" },
    { leftside: "D", rightside: "c D" },
    { leftside: "D", rightside: "b" }
];

let grammar = [
    { leftside: "S", rightside: "E" },
    { leftside: "E", rightside: "T + E" },
    { leftside: "E", rightside: "T" },
    { leftside: "T", rightside: "F * T" },
    { leftside: "T", rightside: "F" },
    { leftside: "F", rightside: "i" }
];
function parser(text) {
    grammar.forEach(rule => {
        rule.rightside = rule.rightside.split(" ");
        for (var i = rule.rightside.length; i >= 0; i--) {
            rule.rightside.splice(i, 0, []);
            rule.rightside[i].index = true;
        }
    });
    find0();
    var ind = 2;
    grammar.forEach(rule => {
        for (var i = 0; i < rule.rightside.length; i += 2) {
            if (rule.rightside[i].length == 0) {
                rule.rightside[i].push(ind);
                find1(ind, rule.rightside[i + 1]);
                //find2(ind, rule.rightside[i + 1]);
                ind++;
            }
        }
    });
    find3();
    grammar.forEach(rule => {
        for (var i = 0; i < rule.rightside.length; i += 2) {
            makeUnique(rule.rightside[i]);
        }
    });
    return grammar;
}

function find0() {
    grammar[0].rightside[0] = [1];
    grammar[0].rightside[0].index = true;
    find1(1, grammar[0].rightside[1]);
    for (var i = 1; i < grammar.length; i++) {
        if (grammar[0].leftside == grammar[i].leftside) {
            grammar[i].rightside[0] = grammar[0].rightside[0];
            find1(1, grammar[i].rightside[1]);
        }
    }
}

function find1(ind, symb) {
    grammar.forEach(rule => {
        if (rule.leftside == symb) {
            if (matchearch(rule.rightside[0], [ind])) {
                return;
            }
            rule.rightside[0].push(ind);
            find1(ind, rule.rightside[1]);
        }
    });
}

// function find2(ind, symb) {
//     grammar.forEach(rule => {
//         for (var i = 0; i < rule.rightside.length; i++) {
//             if (!rule.rightside[i].index) {
//                 if (rule.rightside[i] == symb) {
//                     rule.rightside[i - 1].push(ind);
//                 }
//             }
//         }
//     });
// }

function find3() {
    grammar.forEach(rule => {
        for (var i = 1; i < rule.rightside.length; i += 2) {
            find31(rule.rightside[i - 1], rule.rightside[i], rule.rightside[i + 1]);
        }
    });
}

function find31(prevind, symb, nextind) {
    grammar.forEach(rule => {
        for (var i = 1; i < rule.rightside.length; i += 2) {
            if (rule.rightside[i] == symb) {
                if (matchearch(prevind, rule.rightside[i - 1])) {
                    rule.rightside[i + 1] = nextind;
                    console.log("AAAAAAAAAAA");
                }
            }
        }
    });
}

function makeUnique(a) {
    for (var q = 1, i = 1; q < a.length; ++q) {
        if (a[q] !== a[q - 1]) {
            a[i++] = a[q];
        }
    }

    a.length = i;
    return a;
}

function matchearch(array1, array2) {
    for (var i = 0; i < array1.length; i++) {
        for (var j = 0; j < array2.length; j++) if (array1[i] == array2[j]) return true;
    }
    return false;
}
