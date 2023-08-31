import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

def tokenize(str_expression):
    """
    Takes in a fully parenthesized symbolic expression as a string. Returns 
    a list of relevant tokens. 

    """
    tokens = []
    numbers = ''
    special = ',.-0123456789'
    for i in range(len(str_expression)):
        ###If its a number, check if the next element is also a number.
        if i < len(str_expression) - 1 and str_expression[i] in special and str_expression[i+1] in special:
            numbers += str_expression[i]
        elif numbers != '':
            numbers += str_expression[i]
            tokens.append(numbers)
            numbers = ''
        elif str_expression[i] != ' ':
            tokens.append(str_expression[i])
            
    return tokens

def parse(tokens):
    """
    Takes in a list of tokens and returns a symbolic expression as an instance of the BinOp class.
    """
    variables = 'abcdefghijklmnopqrstuvwxyz'
    def parse_expression(index):
        ##Base case.
        ##If token[index] is a positive or negative number return the number as a Num() object.
        ##If it is a variable return it as a Var() object.
        if tokens[index].isdigit() or (len(tokens[index]) > 1 and tokens[index][1:].isdigit()):
            return (Num(int(tokens[index])), index + 1)
        if tokens[index].lower() in variables:
            return (Var(tokens[index]), index + 1)
        
        ###Recursive call
        ###If token[index] is not in the base cases then it must be an open parenthesis.
        left, index = parse_expression(index + 1)
        operator = tokens[index] 
        right, index = parse_expression(index + 1) 
        
        if operator == '+':
            return (left + right, index + 1)
        elif operator == '-':
            return  (left - right, index + 1)
        elif operator == '*':
            return (left*right, index + 1)
        elif operator == '/':
            return (left/right, index + 1) 
            
    parsed_expression, next_index = parse_expression(0)
    return parsed_expression 

def sym(string_expression):
    """
    Takes in a symbolic expression as a string, returns a symbolic expression 
    as an instance of the BinOp class.
    """
    tokens = tokenize(string_expression)
    return parse(tokens)
        
class Symbol:
    def __add__(self, right):
        return Add(self, right)
    def __radd__(self, right):
        return Add(right, self)
    def __sub__(self, right):
        return Sub(self, right)
    def __rsub__(self, right):
        return Sub(right, self)
    def __mul__(self, right):
        return Mul(self, right)
    def __rmul__(self, right):
        return Mul(right, self)
    def __truediv__(self, right):
        return Div(self, right)
    def __rtruediv__(self, right):
        return Div(right, self)      

class Var(Symbol):
    class_name = 'Var'
    pemdas = 0
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n
        
    def deriv(self, x):
        """ Takes in a variable with which to take the derivative to for a Var() object.
        """
        if self.name == x:
            return Num(1)
        else:
            return Num(0)
        
    def simplify(self):
        """ Simplification rule for a Var() object
        """
        return self
    
    def eval(self, mapping):
        """ Takes in a dictionary mapping each variable to a number. Returns 
            the corresponding int or float values.
        """
        for var in mapping:
            if var == self.name:
                return mapping[var]
        return self
            
    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'


class Num(Symbol):
    class_name = 'Num'
    pemdas = 0
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n
        
    def deriv(self, x):
        """ Takes in a vaariable, x, with which to derive a Num() object 
        """
        return Num(0)
        
    def simplify(self):
        """ Simplification rule for a Num() object. 
        """
        return self
    
    def eval(self, mapping):
        """  Takes in a dictionary mapping each variable to a number. Returns the 
             corresponding int or float values.
        """
        return self.n 

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'
    
class BinOp(Symbol):
    def __init__(self, left, right):
        """ Takes in left and right members of the binary operation, turns 
            them into either Var(), Num(), or Binary Operation objects, and initializes an object
            belonging to a subclass of BinOp().
        """
        for instance in [left, right]:
            if isinstance(instance, str):
                if instance == left:
                    left = Var(instance)
                else:
                    right = Var(instance)
            elif isinstance(instance, float) or isinstance(instance, int):
                if instance == left:
                    left = Num(instance)
                else:
                    right = Num(instance)
        self.left = left
        self.right = right
        
    def helper(self, mapping):
        """ Check if left and right are int or float and convert to Num() 
        """
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        
        digits = ".-0123456789"
        if repr(left)[0] in digits:
            left = Num(left) 
        if repr(right)[0] in digits: 
            right = Num(right)
             
        return left, right
        
    def __str__(self):
        """
        Prints each operation, following pemdas rules for parenthisizing. 
        """
        
        left_string = str(self.left)
        right_string = str(self.right)
        if (self.class_name == 'Sub' or self.class_name == 'Div') and (self.pemdas == self.right.pemdas) and(self.right.pemdas != 0):
            right_string = '(' + str(self.right) + ')'
        if self.pemdas > self.right.pemdas and self.right.pemdas != 0:
            right_string = '(' + str(self.right) + ')'
        if self.pemdas > self.left.pemdas and self.left.pemdas != 0:
            left_string = '(' + str(self.left) + ')'
        
        return left_string + ' ' + self.operand + ' ' + right_string 

    def __repr__(self):
        return '(' + repr(self.left) + ', ' + repr(self.right) + ')'   
    
class Add(BinOp):
    class_name = 'Add'
    operand = '+'
    pemdas = 1
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        
    def deriv(self, x):
        """ Derivatio rules for addition.
        """
        return self.left.deriv(x) + self.right.deriv(x)
        
    def simplify(self):
        """ Simplification rules for addition.
        """
        left = self.left.simplify()
        right = self.right.simplify()
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return Num(left.n + right.n)
        elif left.class_name == 'Num' and left.n == 0:
            return right
        elif right.class_name == 'Num' and right.n == 0:
            return left
        else:
            return left + right
        
    def eval(self, mapping):
        """ Takes in a dictionary mapping variable names to ints or floats. Returns 
            the solution to the equation after substituting those numbers for the variables.
        """
        ###Check if left and right are int or float and convert to Num.
        left, right = self.helper(mapping)
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return left.n + right.n  ##Return an int or float instead of Num()
        elif left.class_name == 'Num' and left.n == 0:
            return right 
        elif right.class_name == 'Num' and right.n == 0:
            return left
        else:
            return left + right
        
        
    def __str__(self):
        return BinOp.__str__(self) 
        
    def __repr__(self):
        return  'Add(' + repr(self.left) + ', ' + repr(self.right) + ')'
    
class Sub(BinOp):
    class_name = 'Sub'
    operand = '-'
    pemdas = 1
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        
    def deriv(self, x):
        return self.left.deriv(x) - self.right.deriv(x)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return Num(left.n - right.n)
        elif right.class_name == 'Num' and right.n == 0:
            return left
        else:
            return left - right
        
    def eval(self, mapping):
        left, right = self.helper(mapping)
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return left.n - right.n
        elif right.class_name == 'Num' and right.n == 0:
            return left
        else:
            return left - right
        
    def __str__(self):
        return BinOp.__str__(self) 
        
    def __repr__(self):
        return  'Sub(' + repr(self.left) + ', ' + repr(self.right) + ')' 
        
class Mul(BinOp):
    class_name = 'Mul'
    operand = '*'
    pemdas = 2
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        
    def deriv(self, x):
        return self.left*self.right.deriv(x) + self.right*self.left.deriv(x)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return Num(left.n*right.n)
        elif left.class_name == 'Num' and left.n == 1:
            return right
        elif right.class_name == 'Num' and right.n == 1:
            return left
        elif left.class_name == 'Num' and left.n == 0:
            return Num(0)
        elif right.class_name == 'Num' and right.n == 0:
            return Num(0)
        else:
            return left*right 
        
    def eval(self, mapping):
        left, right = self.helper(mapping)
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return left.n*right.n
        elif left.class_name == 'Num' and left.n == 1:
            return right
        elif right.class_name == 'Num' and right.n == 1:
            return left
        elif left.class_name == 'Num' and left.n == 0:
            return Num(0)
        elif right.class_name == 'Num' and right.n == 0:
            return Num(0)
        else:
            return left*right 
        
    def __str__(self):
        return BinOp.__str__(self) 
        
    def __repr__(self):
        return  'Mul(' + repr(self.left) + ', ' + repr(self.right) + ')'
    
class Div(BinOp):
    class_name = 'Div'
    operand = '/'
    pemdas = 2
    def __init__(self, left, right):
        BinOp.__init__(self, left, right)
        
    def deriv(self, x):
        numerator = self.left.deriv(x)*self.right - self.right.deriv(x)*self.left
        denominator = self.right*self.right
        return numerator/denominator 
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return Num(left.n/right.n)
        elif right.class_name == 'Num' and right.n == 1:
            return left
        elif left.class_name == 'Num' and left.n == 0:
            return Num(0) 
        else:
            return left/right
        
    def eval(self, mapping):
        left, right = self.helper(mapping)
        
        ###IF SPECIAL CASE: DO SPECIAL THING. ELSE: ADD LEFT AND RIGHT
        if left.class_name == 'Num' and right.class_name == 'Num':
            return left.n/right.n
        elif right.class_name == 'Num' and right.n == 1:
            return left
        elif left.class_name == 'Num' and left.n == 0:
            return Num(0) 
        else:
            return left/right
        
    def __str__(self):
        return BinOp.__str__(self) 
        
    def __repr__(self):
        return  'Div(' + repr(self.left) + ', ' + repr(self.right) + ')'

if __name__ == '__main__':
    doctest.testmod()


