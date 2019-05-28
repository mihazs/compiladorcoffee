 # ------------------------------------------------------------
 # UNIVERIDADE FEDERAL DE SANTA CATARINA
 # CONSTRUCAO DE COMPILADORES
 # Compilador Linguagem Coffee - Analisador Lexico
 # ------------------------------------------------------------
import ply.lex as lex
import tables as tb
import lib

 # ------------------------------------------------------------
 # COMO USAR?
 # 1 - Escreva um pequeno codigo na variavel "data" na linha (84)
 # 2 - Rode o codigo utilizando python3 de preferencia
 # ------------------------------------------------------------
_STACK = []

states = (
    ('multiLineComment','exclusive'),
)


reserved = {
    'if' : 'IF',
    'do' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'int' : 'INT',
    'string' : 'STRING',
    'for' : 'FOR',
    'double' : 'DOUBLE',
    'float' : 'FLOAT_TYPE',
    'main' : 'MAIN',
    'fim' : 'FIM',
    'inicio' : 'INICIO',
    'cout' : 'COUT',
    'cin' : 'CIN',
    'char' : 'CHAR',
    'return' : 'RETURN',
    'integer' : 'INTEGER'

}

tokens = [
    # 'MULTI_COMMENT',
    'FLOAT',
    'LITERAL',
    'INT_VAL',
    'PLUS',
    'PLUSP',
    'MINUS',
    'MINUSM',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8',
    'RES1','RES2','RES3','RES4','RES5','RES6', 'RES7', 'RES8',
    'LOOP1', 'LOOP2', 'LOOP3',
    'TYPE1','TYPE2','TYPE3','TYPE4','TYPE5','TYPE6',
    'NAME'
] + list(reserved.values())


# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_PLUSP    = r'\+\+'
t_MINUS   = r'\-'
t_MINUSM   = r'\-\-'
t_TIMES   = r'\*'
t_DIVIDE  = r'\/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


#COMPARATORS
t_COM1    = r'\>'
t_COM2    = r'\<+'
t_COM3    = r'\>\='
t_COM4    = r'\<\='
t_COM5    = r'\=\='
t_COM6    = r'\!\='
t_COM7    = r'\<\<'
t_COM8    = r'\>\>'

#RESERVEDS
t_RES1    = r'\{'
t_RES2    = r'\}'
t_RES3    = r'\;'
t_RES4    = r'\:'
t_RES5    = r'\,'
t_RES6    = r'\='
t_RES7    = r'\"'
t_RES8    = r'\$'



def main():
    # Build the lexer
    lexer = lex.lex()

    data = '''
    void main {
        v1, v2: integer;
        z : string;
        v3 = 5;
        v4 = 2.35; 
        v5 = 0;
        v6 = "ola";
        cout >> v6;
        \* test comment */
        integer soma[integer; integer){
            inicio
            v7 : integer;
            v8 = v9 + v10;
            return v8;	
            fim
        }
        z = soma(integer; integer);
    }
    '''
    print(data)
    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print (tok.type, tok.value, tok.lineno, tok.lexpos)
        lib.classify(tok.value, tok.type, tok.lineno)
    
    lib.prepare()


# A regular expression rule with some action code

def t_NAME(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
     return t

def t_multiLineComment_start(t):
    r'/\*'
    t.lexer.begin('multiLineComment')          

def t_multiLineComment_end(t):
    r'\*/'
    t.lexer.begin('INITIAL')           

def t_multiLineComment_newline(t):
    r'\n'
    pass

# catch (and ignore) anything that isn't end-of-comment
def t_multiLineComment_content(t):
    r'[^(\*/)]'
    pass


def t_FLOAT(t):
    r'(\d*\.\d+)|(\d+\.\d*)'
    # a better regex taking exponents into account:     
    t.value = float(t.value)
    return t

# Read in a string, as in C.  The following backslash sequences have their 
# usual special meaning: \", \\, \n, and \t.
def t_LITERAL(t):
    r'\"([^\\"]|(\\.))*\"'
    escaped = 0
    str = t.value[1:-1]
    new_str = ""
    for i in range(0, len(str)):
        c = str[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = 0
        else:
            if c == "\\":
                escaped = 1
            else:
                new_str += c
    t.value = new_str
    return t


def t_INT_VAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("[+] Illegal character '%s' in line '%d' " % (t.value[0], t.lineno))
    t.lexer.skip(1)



main()

