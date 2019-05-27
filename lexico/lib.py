import tables as tb

_STACK = []

def classify(token, typ, line):
    for t in tb._TYPES:
        if(t['string'] == token):
            _STACK.append([t['token'], token, line]) # ADICIONANDO A PILHA
            return t
    #TOKEN OPERATORS
    for t in tb._OPERATORS:
        if(t['string'] == token):
            _STACK.append([t['token'], token, line]) # ADICIONANDO A PILHA
            return t

    #TOKEN LOOPS
    for t in tb._LOOPS:
        if(t['string'] == token):
            _STACK.append([t['token'], token, line]) # ADICIONANDO A PILHA
            return t

    #TOKEN RESERVEDS
    for t in tb._RESERVEDS:
        if(t['string'] == token):
            _STACK.append([t['token'], token, line]) # ADICIONANDO A PILHA
            return t

    #TOKENS DECISION
    for t in tb._DECISION:
        if(t['string'] == token):
            _STACK.append([t['token'], token, line]) # ADICIONANDO A PILHA
            return t

    if(typ == "INT_VAL"):
        _STACK.append([5, token, line]) # ADICIONANDO A PILHA

    if(typ == "FLOAT"):
        _STACK.append([6, token, line]) # ADICIONANDO A PILHA
    
    if(typ == "LITERAL"):
        _STACK.append([12, token, line]) # ADICIONANDO A PILHA
    
    if(typ == "NAME"):
        _STACK.append([99, token, line])
    
    if(typ == "STRING"):
        _STACK.append([10, token, line])


#PREPARA OS TOKENS NAMES PARA CLASSIFICAR ELES EM FUNCAO OU NOMEDEVARIAVEL
def prepare():
    i = 0
    #PREPARANDO NOMES SE SAO FUNCAO OU VARIAVEIS
    for s in _STACK:
        if(s[0] == 99):
            check(s[1], i)
        i += 1

    print_stack()


def check(name, pos):
    prox = _STACK[pos+1][1]
    ante =  _STACK[pos-1][1]
    #print("token recebido:"+name)
    #print("Prox:" + prox)
    #print("Antes:" + ante)

    if(prox == '(' ):
        _STACK[pos][0] = 27 #recebe o token id de chamada de funcao
    
    if(prox == ',' or prox == '='):
        _STACK[pos][0] = 9

    #contrucoes do tipo var = var+/operator/+var;
    if(ante == '=' and prox == "+" or prox == "-" or prox == "/" or prox == "*"):
        _STACK[pos][0] = 9

    #contrucoes do tipo var = var+/operator/+var;
    if(ante == ';' and prox == "," or prox == "="):
        _STACK[pos][0] = 9
    
    if(prox == ';' and ante == "+" or ante == "-" or ante == "/" or ante == "*"):
        _STACK[pos][0] = 9
    
    if(ante == 'return' or prox == ":"):
        _STACK[pos][0] = 9
    
    if(ante == "<<" or ante == ">>"):
        _STACK[pos][0] = 9
    

def print_stack():
    print("LISTA DE TOKENS:")
    print("---------------------------------")
    for s in _STACK:
        print("token_id: "+str(s[0]) + " | lexema: "+str(s[1]) + " | linha: "+str(s[2]) )
