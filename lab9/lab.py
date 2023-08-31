#!/usr/bin/env python3
"""6.009 Lab 9: Snek Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!

################
# Environments # 
################

class Function:
    def __init__(self, arguments, body, environment):
        """Takes in arguments as a list of strings, body as a parsed S-expression,
           and environment as an environment object.
        """
        self.args = arguments
        self.body = body 
        self.env = environment 
        
    def __call__(self, arguments):  
        if len(arguments) != len(self.args):
            raise SnekEvaluationError
            
        new_frame = Environment('new_frame', {}, self.env)  
        for variable, value in zip(self.args, arguments): 
            new_frame.vars[variable] = value
        return evaluate(self.body, new_frame)   
        
        
    def __repr__(self):
        return f"function<args>{self.args}<body>{self.body}"
    def __str__(self):
        return f"function<args>{self.args}<body>{self.body}" 



class Environment:
    def __init__(self, name, variables, parent = None):
        """
        Takes in parent, another Enviroment obect, variables, a dictionary
        mapping variable names (str) to values, and a name (str).
        """
        self.name = name
        self.parent = parent
        self.vars = variables
        
    def var_in_environment(self, var):
        if isinstance(var, list):
            var = evaluate(var, self)
        return var in self.vars
    def var_exist(self, var):
        """ Recursive procedure checks if var is in any of the environments
        """
        if isinstance(var, list):
            return False
        if self.var_in_environment(var):
            return True
        if self.parent == None:
            return False
        return self.parent.var_exist(var)  
    def get_var(self, var):
        """ Recursive procedure gets variable value in the parent environment
            if its not in the local environment.
        """
        if self.var_in_environment(var):
            return self.vars[var]
        if self.parent == None: 
            raise SnekNameError 
        return self.parent.get_var(var)
    def __repr__(self):
        return self.name
    def __str__(self):
        return f"Parent: {self.parent.name}. Variables: {self.vars}" 
    
###########################
# Snek-related Exceptions #
###########################

class SnekError(Exception):
    """
    A type of exception to be raised if there is an error with a Snek
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass


class SnekSyntaxError(SnekError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    def __str__(self):
        return 'Malformed expression.'
    
    def __repr__(self):
        return 'Malformed expression.'

class SnekNameError(SnekError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    def __str__(self):
        return 'Name has not been defined.'
    
    def __repr__(self):
        return 'Name has not been defined.'


class SnekEvaluationError(SnekError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SnekNameError.
    """
    def __str__(self):
        return 'Error during evaluation.'
    
    def __repr__(self):
        return 'Error during evaluation.'


############################
# Tokenization and Parsing #
############################


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    """
    flag = True
    token = ''
    tokens = []
    for i in range(len(source)):
        if source[i] == ';': 
            flag = False
        if source[i] == '\n':
            flag = True
            
        if flag and source[i] != ' ' and source[i] != '\n' and source[i] != '(' and source[i] != ')':
            token += source[i]
        if token != '' and (source[i] == ' ' or source[i] == '\n' or i == len(source) - 1 or source[i] == '(' or source[i] == ')'):
            tokens.append(token) 
            token = '' 
        if flag and (source[i] == '(' or source[i] == ')'):
            tokens.append(source[i])
            
    return tokens
    
def parse(tokens):
    """
    Takes in a list of tokens and returns a symbolic expression as an instance of the BinOp class.
    """
    ##Some SnekSyntaxErrors
    ###Errors relating to number and position of parenthesis
    open_parenthesis = 0
    close_parenthesis = 0
    prev = '.'
    if tokens[0] == ')' or tokens[-1] == '(':
        raise SnekSyntaxError
    for elem in tokens:
        if elem == '(':
            open_parenthesis += 1
        elif elem == ')':
            close_parenthesis += 1
        elif prev == '(' and elem == ')':
            raise SnekSyntaxError
    if open_parenthesis != close_parenthesis:
        raise SnekSyntaxError
    if tokens[0] in snek_builtins:
            raise SnekSyntaxError
    def parse_expression(index):
        """ Main chunck of parsed function. Works recursively to search for parenthesese 
           and S-expressions through the tokens to recunstruct the tokenized input as a list of 
           S-expressions
        """
        
        ##More SnekSyntaxErrors 
        ###If a token is a list or parenthesis are not tokenized (ex: '(hello)' as one token).
        if isinstance(tokens[index], list):
            raise SnekSyntaxError
        if (tokens[index][0] == '(' or tokens[index][-1] == ')') and len(tokens[index]) > 1:
            raise SnekSyntaxError 
            
        ##Base case.
        ###If token is a positive or negative int.
        if tokens[index].isdigit() or (len(tokens[index]) > 1 and tokens[index][1:].isdigit()) and tokens[index][0] == '-':
            return (int(tokens[index]), index)
        ###If token is a float.
        elif '.' in tokens[index] and len(tokens[index]) > 1:
            token_list = [char for char in tokens[index]]
            token_list.remove('.')
            new_token = ''.join(token_list)
            if new_token.isdigit() or (len(new_token) > 1 and new_token[1:].isdigit()) and new_token[0] == '-':
                return (float(tokens[index]), index)
        ###If token is a word.
        if tokens[index] != '(' and tokens[index] != ')': 
            return (tokens[index], index) 
        
        ###Recursive call
        ###If token[index] is not in the base cases then it must be a parenthesis.
        magic_list = []        
        while index + 1 < len(tokens): 
            ###if the end of the list is reached.
            if index + 1 == len(tokens) - 1:
                return (magic_list, index)  
            ###If we find a closing parenthesis.
            if tokens[index + 1] == ')':
                return (magic_list, index) 
            ###Else we have an open parenthesis which we return as a list.
            expression = parse_expression(index + 1) 
            magic_list += [expression[0]]
            index = expression[1]
            ###If we find a list it means it was a parenthesized expression which was
            ###Recursively converted to a list. Concatenate that list with the result
            ### of the recursive call.
            if isinstance(expression[0], list):
                expression = parse_expression(index + 1)
                magic_list += expression[0] 
                index = expression[1]
            
    parsed_expression, index = parse_expression(0)   
    
        
    ###Error for parenthesized number
    if isinstance(parsed_expression, list) and len(parsed_expression) == 1:
        if isinstance(parsed_expression[0], int) or isinstance(parsed_expression[0], float):
            raise SnekSyntaxError
    ###Errors relating to assignment operand
    if isinstance(parsed_expression, list):
        if parsed_expression[0] == ':=':
            if len(parsed_expression) != 3:
                raise SnekSyntaxError
            elif isinstance(parsed_expression[1], str) == False and isinstance(parsed_expression[1], list) == False:
                raise SnekSyntaxError
            elif parsed_expression[1] == []: 
                raise SnekSyntaxError
            elif isinstance(parsed_expression[1], list): 
                for i in parsed_expression[1]:
                    if not isinstance(i, str):
                        raise SnekSyntaxError
            
        ###Errors relating to function operand.
        elif parsed_expression[0] == 'function':
            if len(parsed_expression) != 3:
                raise SnekSyntaxError
            elif isinstance(parsed_expression[1], list) == False:
                raise SnekSyntaxError
            else:
                for i in parsed_expression[1]:
                    if not isinstance(i,str):
                        raise SnekSyntaxError
    return parsed_expression


######################
# Built-in Functions #
######################

def mult(args):
    """ Performs a multiplication according to the rules discussed in the assingment website.
    """
    prev = 1
    for elem in args:
        prev *= elem 
    return prev

def div(args):
    """ Performs a division according to the rules discussed in the assingment website.
    """
    if len(args) == 0:
        raise SnekEvaluationError
    if len(args) == 1:
        return 1/args[0]
    
    prev = args[0]
    for elem in args[1:]:
        prev /= elem 
    return prev 

def assign(args, environment):
    """ Takes in an assignment S-expression, i.e. (:= variable value), and an environment.
        Assigns the corrsponding value to a variable in the environment's self.vars dictionary.
    """
    variable = args[0]
    if len(args) != 2:
        raise SnekSyntaxError  
    if isinstance(args[0], list):
        if len(args[0]) == 1:
            variable = args[0][0]
            environment.vars[variable] = Function([], args[1], environment)
            return Function([], args[1], environment)
        elif len(args[0]) > 1:
            variable = args[0][0]
            environment.vars[variable] = Function(args[0][1:], args[1], environment)
            return Function(args[0][1:], args[1], environment)
        
    environment.vars[variable] = evaluate(args[1], environment) 
    return evaluate(args[1], environment) 
        
        
snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else 0 if len(args) == 0 else (args[0] - sum(args[1:])), 
    '*': mult,
    '/': div,
    ':=': assign,
    'function': 0, 
}

builtins = Environment('builtins', snek_builtins)

##############
# Evaluation #
##############


def evaluate(tree, environment = None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    
    ##If no environment is passed initialize to empty environment.
    if environment == None:
        environment = Environment('empty', {}, builtins) 
        
    if isinstance(tree, float) or isinstance(tree, int):
        ###If input is a number.
        return tree
    elif isinstance(tree, list) and (isinstance(tree[0], list) or environment.var_exist(tree[0])):
        ###If input is an S-expression.
        if tree[0] == ':=':
            return environment.get_var(tree[0])(tree[1:], environment)
        elif tree[0] == 'function':
            return Function(tree[1], tree[2], environment) 
        elif isinstance(tree[0], list):
            tree_zero = [evaluate(tree[0], environment)]
            tree = tree_zero + tree[1:] 
            return evaluate(tree, environment)
        else:
            if len(tree) == 1 and not isinstance(evaluate(tree[0], environment), Function): 
                raise SnekSyntaxError
            args = []
            for elem in tree[1:]: 
                if isinstance(elem, int) == False or isinstance(elem, float) == False:
                    args.append(evaluate(elem, environment))
                else:
                    args.append(elem) 
            return environment.get_var(tree[0])(args) 
    elif isinstance(tree, list) and isinstance(tree[0], Function):
        ###If the first element of the expression is a function object.
        new_tree = [evaluate(elem, environment) for elem in tree[1:]]
        return tree[0](new_tree) 
    elif isinstance(tree, list) and tree[0] not in snek_builtins.values():  
        ###ifthe first element of an S-expression is not defined.
        raise SnekEvaluationError 
    elif isinstance(tree, list) == False and environment.var_exist(tree):
        ###If it is a defined variable.
        return environment.get_var(tree)
    elif isinstance(tree, Function): 
        ###If input is a function object.
        return tree
    else:
        ###If none of these, then input is a variable that is not defined.
        raise SnekNameError
        
def result_and_env(tree, environment = None): 
    """ performs the same function as evaluate except it returns the environment
        evaluate is working with as well.
    """
    if environment == None:
        environment = Environment('empty', {}, builtins)

    return (evaluate(tree, environment), environment) 
                
def repl():
    """ repl for testing.
    """
    x = 0
    environment = Environment('empty', {}, builtins)
    while x != 'QUIT': 
        try:
            try:
                try:  
                    x = input('in>\t')
                    if x != 'QUIT':
                        print('  out> ', evaluate(parse(tokenize(x)), environment)) 
                except SnekNameError: 
                    print('SnekNameError')
            except SnekSyntaxError:
                print('SnekSyntaxError')
        except SnekEvaluationError:
            print('SnekEvaluationError') 
            
           
           
            
    

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    
    # environment = Environment('empty', {}, builtins)
    # print(environment.get_vars())
    # print(environment.get_var('+'))
    # tokens1 = tokenize('(:= (+ x y) (* x y))')
    # parsed1 = parse(tokens1)
    # eval1 = evaluate(parsed1, environment)
    # print(environment.get_vars())
    # print(environment.get_var('+')) 
    # tokens2 = tokenize('(+ 2 3)')
    # parsed2 = parse(tokens2)
    # eval2 = evaluate(parsed2, environment)
    # print(environment.get_vars())
    # print(environment.get_var('+'))
     # tokens = tokenize('(:=)')
     # parsed = parse(tokens)
     # print(tokens)
     # print(parsed)
      # repl()
     pass
    