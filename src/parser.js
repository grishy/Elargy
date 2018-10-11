let grammar2 = [
    { leftside: 'S', rightside: 'A' },
    { leftside: 'S', rightside: 'D' },
    { leftside: 'A', rightside: 'a b' },
    { leftside: 'A', rightside: 'a c' },
    { leftside: 'A', rightside: 'A b' },
    { leftside: 'D', rightside: 'c D' },
    { leftside: 'D', rightside: 'b' }
];

class parser {
    constructor(text) {
        //Грамматика
        this.grammar = [
            { leftside: 'S', rightside: 'E' },
            { leftside: 'E', rightside: 'T PLUS E' },
            { leftside: 'E', rightside: 'T' },
            { leftside: 'T', rightside: 'F MULT T' },
            { leftside: 'T', rightside: 'F' },
            { leftside: 'F', rightside: 'INTEGER' }
        ];
        let i = 1;
        this.grammar.forEach(rule => {
            rule.num = i++;
            rule.rightside = rule.rightside.split(' ');
            rule.rightside.characters = rule.rightside.length;
            for (let i = rule.rightside.length; i >= 0; i--) {
                rule.rightside.splice(i, 0, []);
                rule.rightside[i].index = true;
            }
        });

        //Таблица разбора
        this.parserTable = [];

        //Терминалы
        this.terminals = this.getTerminals();
        //Нетерминалы
        this.noterminals = this.getNoTerminals();
        //Аксиома
        this.axiom = this.noterminals[0];
        this.indexesByRule1();
        let ind = 2;
        this.grammar.forEach(rule => {
            for (let i = 0; i < rule.rightside.length; i += 2) {
                if (rule.rightside[i].length == 0) {
                    rule.rightside[i].push(ind);
                    this.indexesByRule2(ind, rule.rightside[i + 1]);
                    ind++;
                }
            }
        });
        this.indexesByRule3();
        this.grammar.forEach(rule => {
            for (let i = 0; i < rule.rightside.length; i += 2) {
                this.unique(rule.rightside[i]);
            }
        });

        this.renderRules();

        //this.renderParserTable(this.parserTable);
        this.grammar[0].rightside.push('$');
        this.makeParserTable();

        console.log(this.parserTable);
        //this.parseString(text);
    }

    indexesByRule1() {
        this.grammar[0].rightside[0] = [1];
        this.grammar[0].rightside[0].index = true;
        this.indexesByRule2(1, this.grammar[0].rightside[1]);
        for (let i = 1; i < this.grammar.length; i++) {
            if (this.grammar[0].leftside == this.grammar[i].leftside) {
                this.grammar[i].rightside[0] = this.grammar[0].rightside[0];
                this.indexesByRule2(1, this.grammar[i].rightside[1]);
            }
        }
    }

    getNoTerminals() {
        let noTerms = [];
        this.grammar.forEach(rule => {
            noTerms.push(rule.leftside);
        });
        return this.unique(noTerms);
    }

    getTerminals() {
        let Terms = [];
        let noTerms = this.getNoTerminals();
        this.grammar.forEach(rule => {
            for (let i = 0; i < rule.rightside.length; i++) {
                if (
                    !this.matchearch([rule.rightside[i]], noTerms) &&
                    rule.rightside[i].index === undefined
                ) {
                    Terms.push(rule.rightside[i]);
                }
            }
        });
        Terms.push('$');
        return this.unique(Terms);
    }

    indexesByRule2(ind, symb) {
        this.grammar.forEach(rule => {
            if (rule.leftside == symb) {
                if (this.matchearch(rule.rightside[0], [ind])) {
                    return;
                }
                rule.rightside[0].push(ind);
                this.indexesByRule2(ind, rule.rightside[1]);
            }
        });
    }

    indexesByRule3() {
        this.grammar.forEach(rule => {
            for (let i = 1; i < rule.rightside.length; i += 2) {
                this.identicalTransitions(
                    rule.rightside[i - 1],
                    rule.rightside[i],
                    rule.rightside[i + 1]
                );
            }
        });
    }

    identicalTransitions(prevind, symb, nextind) {
        this.grammar.forEach(rule => {
            for (let i = 1; i < rule.rightside.length; i += 2) {
                if (rule.rightside[i] == symb) {
                    if (this.matchearch(prevind, rule.rightside[i - 1])) {
                        rule.rightside[i + 1] = nextind;
                    }
                }
            }
        });
    }

    unique(arr) {
        let obj = {};

        for (let i = 0; i < arr.length; i++) {
            let str = arr[i];
            obj[str] = true;
        }

        return Object.keys(obj);
    }

    matchearch(array1, array2) {
        for (let i = 0; i < array1.length; i++) {
            for (let j = 0; j < array2.length; j++) if (array1[i] == array2[j]) return true;
        }
        return false;
    }

    renderRules() {
        this.grammar.forEach(rule => {
            let newstr = rule.leftside + ' => ';
            for (let i = 0; i < rule.rightside.length; i++) {
                if (rule.rightside[i].index == true) {
                    newstr += '<sub>' + rule.rightside[i] + '</sub>';
                } else {
                    newstr += rule.rightside[i];
                }
            }
            $('ol').append('<li>' + newstr + '</li>');
        });
    }

    makeParserTable() {
        //SHIFT
        this.grammar.forEach(rule => {
            for (let i = 1; i < rule.rightside.length; i += 2) {
                rule.rightside[i - 1].forEach(ind => {
                    this.parserTable[ind + rule.rightside[i]] = 'S' + rule.rightside[i + 1];
                });
            }
        });
        //REDUCE
        this.findReduceComand();
        //ACCEPT
        this.parserTable[1 + this.axiom] = 'ACCEPT';
    }

    findReduceComand() {
        let columns = [];
        let cell = [];
        this.noterminals.forEach(term => {
            columns = this.findNextTerminal(term);
            cell = this.findProduce(term);
            columns.forEach(col => {
                cell.forEach(c => {
                    this.parserTable[this.findLastIndex(c) + col] = 'R' + (c + 1);
                });
            });
        });

        let cellS = this.findProduce('S');
        cellS.forEach(c => {
            this.parserTable[this.findLastIndex(c) + '$'] = 'R' + (c + 1);
        });
    }

    findProduce(leftside) {
        let finded = [];
        for (let i = 0; i < this.grammar.length; i++) {
            if (this.grammar[i].leftside == leftside) {
                finded.push(i);
            }
        }
        return finded;
    }

    findLastIndex(numrule) {
        let lastind;
        for (let i = 0; i < this.grammar[numrule].rightside.length; i++) {
            if (this.grammar[numrule].rightside[i].index != undefined)
                lastind = this.grammar[numrule].rightside[i][0];
        }
        return lastind;
    }

    findNextTerminal(LSide) {
        let finded = [];
        this.grammar.forEach(rule => {
            for (let i = 1; i < rule.rightside.length; i += 2) {
                if (rule.rightside[i] == LSide) {
                    if (rule.rightside.length == 1 + 2) {
                        finded = finded.concat(this.findNextTerminal(rule.leftside));
                    }
                    if (i + 2 < rule.rightside.length) {
                        finded.push(rule.rightside[i + 2]);
                    }
                }
            }
        });

        return finded;
    }

    // tableTransform(){
    //     this.parserTable.forEach(element => {
    //         element = {head: element.row + element.column, command: element.cell}
    //     });
    //     console.log(this.parserTable);
    // }

    parseString(text) {
        let characterStack = [];
        let statesStack = [1];
        text.push({ token: '$' });
        let command;
        let incoming;
        let i = 0;
        let j = 25;
        let del = 0;
        while(j--){
            incoming = text[i].token;
            console.log(statesStack[statesStack.length - 1], incoming);
            command = this.tableSearch(statesStack[statesStack.length - 1], incoming);
            console.log('Команда:',command);
            console.log('Стэк состояний:', statesStack);
            console.log('Стэк символов:', characterStack);
            console.log('Входящий символ:', incoming);
            console.log('i: ', i);
            console.log(del);
            if(command == false){
                console.log('ОШИБКА!');
                return;
            } else if(command == 'ACCEPT'){
                console.log('Строка успешно разобрана!');
                return;
            } else if(command[0] == 'S'){
                characterStack.push(incoming);
                statesStack.push(command.slice(1));
                i++;
            } else if(command[0] == 'R'){
                characterStack.splice(- del, del);
                del = this.grammar[Number(command.slice(1)) - 1].rightside.characters;
                statesStack.splice(- del, del);
                text.splice(i, 0, { token: this.grammar[Number(command.slice(1)) - 1].leftside});
            }
            console.log('---------------------------');
            
        }
    }

    tableSearch(state, symb) {
        console.log(this.parserTable[state + symb]);
        if (this.parserTable[state + symb] != undefined) return this.parserTable[state + symb];
        else return false;
    }


}
