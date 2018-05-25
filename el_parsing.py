import copy
import json

class ElParser:
    HTMLPAGE = '''
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <div class="tree">
            <ul>
                RRRRR
            </ul>
        </div>
    </body>

    <style>
        /*Now the CSS*/
        * {
            margin: 0; padding: 0;
        }

        .tree ul {
            padding-top: 20px; position: relative;
            
            transition: all 0.5s;
            -webkit-transition: all 0.5s;
            -moz-transition: all 0.5s;
        }

        .tree li {
            float: left; text-align: center;
            list-style-type: none;
            position: relative;
            padding: 20px 5px 0 5px;
            
            transition: all 0.5s;
            -webkit-transition: all 0.5s;
            -moz-transition: all 0.5s;
        }

        /*We will use ::before and ::after to draw the connectors*/

        .tree li::before, .tree li::after{
            content: '';
            position: absolute; top: 0; right: 50%;
            border-top: 1px solid #ccc;
            width: 50%; height: 20px;
        }
        .tree li::after{
            right: auto; left: 50%;
            border-left: 1px solid #ccc;
        }

        /*We need to remove left-right connectors from elements without 
        any siblings*/
        .tree li:only-child::after, .tree li:only-child::before {
            display: none;
        }

        /*Remove space from the top of single children*/
        .tree li:only-child{ padding-top: 0;}

        /*Remove left connector from first child and 
        right connector from last child*/
        .tree li:first-child::before, .tree li:last-child::after{
            border: 0 none;
        }
        /*Adding back the vertical connector to the last nodes*/
        .tree li:last-child::before{
            border-right: 1px solid #ccc;
            border-radius: 0 5px 0 0;
            -webkit-border-radius: 0 5px 0 0;
            -moz-border-radius: 0 5px 0 0;
        }
        .tree li:first-child::after{
            border-radius: 5px 0 0 0;
            -webkit-border-radius: 5px 0 0 0;
            -moz-border-radius: 5px 0 0 0;
        }

        /*Time to add downward connectors from parents*/
        .tree ul ul::before{
            content: '';
            position: absolute; top: 0; left: 50%;
            border-left: 1px solid #ccc;
            width: 0; height: 20px;
        }

        .tree li a{
            border: 1px solid #ccc;
            padding: 5px 10px;
            text-decoration: none;
            color: #666;
            font-family: arial, verdana, tahoma;
            font-size: 11px;
            display: inline-block;
            
            border-radius: 5px;
            -webkit-border-radius: 5px;
            -moz-border-radius: 5px;
            
            transition: all 0.5s;
            -webkit-transition: all 0.5s;
            -moz-transition: all 0.5s;
        }

        /*Time for some hover effects*/
        /*We will apply the hover effect the the lineage of the element also*/
        .tree li a:hover, .tree li a:hover+ul li a {
            background: #c8e4f8; color: #000; border: 1px solid #94a0b4;
        }
        /*Connector styles on hover*/
        .tree li a:hover+ul li::after, 
        .tree li a:hover+ul li::before, 
        .tree li a:hover+ul::before, 
        .tree li a:hover+ul ul::before{
            border-color:  #94a0b4;
        }

        /*Thats all. I hope you enjoyed it.
        Thanks :)*/
    </style>
</html>
'''


    def __init__(self, grammar, table, lex):
        self.gm = grammar
        self.tl = table
        self.lx = lex
        self.lx.addToken("$",0,0)
        self.tree = {}

        operation = ''
        ind = 0
        states = [1]
        symbols =''
        yyy = 0 
        
        while True:
            symb = self.lx.tokens[ind]
            t = symb['typ']
            st = states[-1]
            # print('Символ')
            # print(self.lx.tokens[ind]['typ'])
            # print('Состояния')
            # print(states)
            # print('Индекс')
            # print(ind)
            try:
                operation = self.tl.table[st][t]
            except:
                operation = 'error'

            
            if(operation == 'admission'):
                self.tree = self.lx.tokens[-2]
                print('ACEPT')
                break
            elif(operation[0] == 'R'):
                rul = self.gm.rules[int(operation[1:])-1]

                ln = len(rul.right_side)
                for x in range(ln):
                    states.pop(-1)

                toks= self.lx.tokens[ind - ln:ind]
                
                # print("*" * 15)
                # print(rul.left_side)
                # print(toks)
                # print("*" * 15)
                ind-=1

                self.lx.tokens[ind] = {
                    'typ': rul.left_side,
                    'child' : toks
                }
                
                
                # parserOut = open('./deb/%s_%s.html' % (ind,yyy), 'w+')
                # parserOut.write(self.toHTML(self.lx.tokens[ind]))
                # parserOut.close()
                # yyy += 1
                
                
                
            elif(operation == 'error'):
                print('PARSE ERROR')
                break
            elif(operation[0] == 'S'):
                states.append(int(operation[1:]))
                ind = ind + 1
     

    def toJSON(self):
        return json.dumps(self.tree, indent=2)

    def nodeToHTML(self,node):
        html = '''
        <li> <a href="#">{}</a> {} </li>
        '''

        hasChild = '''
        <ul> {} </ul>
        '''
        
        if "child" in node:
            allChild =  "\n".join([self.nodeToHTML(c) for c in node["child"]])
            htmlChild = "<ul> {} </ul>".format(allChild)
            return html.format(node["typ"],htmlChild)
        else:
            text = "<b>{}: {}</b>".format(node["typ"], node["val"])
            return html.format(text,"")

    def toHTML(self, root):
        intro = self.nodeToHTML(root)
        out = self.HTMLPAGE.replace("RRRRR",intro)
        return out
