import sys
from lark import Lark, Tree, Token, UnexpectedInput, UnexpectedToken, UnexpectedCharacters


with open('grammar.lark', 'r') as f:
    grammar = f.read()
#print(grammar)
parser = Lark(grammar, start='start', parser='lalr',cache=False)

############################
def print_num(val):
    print(val)

def print_bool(val):
    if (val):
        print("#t")
    else:
        print("#f")

def plus(*nums):
    for n in nums:
        if type(n) is not int:
            print("Type error! plus need int ")
            exit(0)
    total=0
    for n in nums:
        total+=n
    return total

def minus(x, y):
    if type(x) is not int | type(y) is not int:
        print("Type error! minus need int")
        exit(0)
    return x - y

def multiply(*nums):
    for n in nums:
        if type(n) is not int:
            print("Type error! mul need int")
            exit(0)
    total=1
    for n in nums:
        total*=n
    return total

def divide(x, y):
    if type(x) is not int | type(y) is not int:
        print("Type error! div need int")
        exit(0)
    if y==0:
        print("div by 0")
        exit(0)

    return int(x) // int(y)

def mod(x, y):
    if type(x) is not int | type(y) is not int:
        print("Type error! mod need int ")
        exit(0)
    return x % y

def greater(x, y):
    if type(x) is not int | type(y) is not int:
        print("Type error! > need int")
        exit(0)
    return x > y

def smaller(x, y):
    if type(x) is not int | type(y) is not int:
        print("Type error! < need int")
        exit(0)
    return x < y

def equal(*nums):
    for n in nums:
        if type(n) is not int:
            print("Type error! = need int")
            exit(0)
    first = nums[0]
    for n in nums:
        if n != first:
            return False
    return True

def and_op(*bools):
    for b in bools:
        if type(b) is not bool:
            print("Type error! and need bool")
            exit(0)
    return all(bools)

def or_op(*bools):
    for b in bools:
        if type(b) is not bool:
            print("Type error! or need bool")
            exit(0)
    return any(bools)

def not_op(b):
    if type(b) is not bool:
        print("Type error! not need bool")
        exit(0)
    return not b

base_func = {
    "print_num": print_num,
    "print_bool": print_bool,
    "plus": plus,
    "minus": minus,
    "multiply": multiply,
    "divide": divide,
    "modulus": mod,
    "greater": greater,
    "smaller": smaller,
    "equal": equal,
    "and_op": and_op,
    "or_op": or_op,
    "not_op": not_op,
}
###################################

class Env(dict):
    def __init__(self, parent=None):
        super().__init__(base_func)
        self.parent = parent

    def lookup(self, name):
        if name in self:
            return self[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            print(f"未定義{name}符號")
            exit(0)

class Function:
    def __init__(self, arg_list, body_node, closure_env):
        self.arg_list = arg_list
        self.body_node = body_node
        self.closure_env = closure_env

    def call(self, *args):
        if len(args) != len(self.arg_list):
            print(f"函式參數個數不符，需要 {len(self.arg_list)} 個，實際呼叫傳入 {len(args)} 個")
            exit(0)
        child_env = Env(parent=self.closure_env)
        for name, val in zip(self.arg_list, args):
            child_env[name] = val
        return interpret_ast(self.body_node, child_env)


def interpret_ast(node, env):
    #tree{value children}
    #token{value type}
    if isinstance(node, Token):
        if node.type == "NUMBER":
            return int(node.value)
        elif node.type == "BOOL_VAL":
            if(node.value=="#t"):
                return True
            elif(node.value=="#f"):
                return False
            else:
                print("error 1")

        elif node.type == "ID":
            return env.lookup(node.value)
        else:
            print("error 2")

    if isinstance(node, Tree):
        rule = node.data

        if rule == "start":
            for child in node.children:
                interpret_ast(child, env)
          
        elif rule == "print_num":
            val = interpret_ast(node.children[0], env)
            return env["print_num"](val)

        elif rule == "print_bool":
            val = interpret_ast(node.children[0], env)
            return env["print_bool"](val)

        elif rule == "def_stmt":
            var, expr = node.children
            var_name = var.value  
            val = interpret_ast(expr, env)
            env[var_name] = val

        elif rule == "if_exp":
            test_node, then_node, else_node = node.children
            condition = interpret_ast(test_node, env)
            if not isinstance(condition, bool):
                print("type error! IF need bool")
                exit(0)
            if condition:
                branch = then_node
            else:
                branch = else_node
            return interpret_ast(branch, env)
        

        elif rule == "fun_exp":
            # fun_exp: "(" "fun" fun_ids fun_body ")"
            # fun_ids: "(" ID* ")"
            # fun_body: expr
            fun_ids_node, fun_body_node = node.children
            param_names = []
            for t in fun_ids_node.children:
                param_names.append(str(t))
            return Function(param_names, fun_body_node, env)

        elif rule == "fun_call":
            # fun_call: "(" fun_exp param* ")" | "(" fun_name param* ")"
            func_node = node.children[0]  
            args_nodes = node.children[1:]
            func_val = interpret_ast(func_node, env)
            call_args= []
            for arg in args_nodes:
                call_args.append(interpret_ast(arg,env))
            return func_val.call(*call_args)
        
        elif rule in ("plus", "minus", "multiply", "divide", "modulus","greater", "smaller", "equal","and_op", "or_op", "not_op"):
            operation = env.lookup(rule)
            arguments = []
            for child in node.children:
                arguments.append(interpret_ast(child, env))
            return operation(*arguments)

        else:
            print(f"不支援的語法: {rule}")
            exit(0)

code = sys.stdin.read()
try:
    tree = parser.parse(code)
    #print(tree)
    #print(tree.pretty())
except (UnexpectedInput, UnexpectedToken, UnexpectedCharacters):
   print("syntax error")
   exit(0)

env = Env()
interpret_ast(tree, env)

