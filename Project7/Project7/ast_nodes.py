import abc
from enum import Enum
from collections import namedtuple

PrimitiveType = Enum('PrimitiveType', 'NUMBR NUMBAR LETTR TROOF')
ArrayType = namedtuple('ArrayType', ['subtype'])
class CompilerTypeError(Exception): pass


class ASTNode(abc.ABC):
    def __init__(self, children=None):
        self.children = children if children else []
        
    def __repr__(self):
        result = type(self).__name__ # class name
        if self.children:
            children_reprs = [repr(child) for child in self.children]
            children_lines = '\n'.join(children_reprs)
            children_lines_tabbed = map(lambda x: '\t' + x, children_lines.splitlines())
            result += '\n' + '\n'.join(children_lines_tabbed)
        return result

    @abc.abstractmethod
    def compile(self, symbol_table, compiled_code):
        for child in self.children:
            child.compile(symbol_table, compiled_code)


########################################################################
class FunctionCall(ASTNode):
    def __init__(self, children):
        super().__init__(children=children)

    def compile(self, symbol_table, compiled_code):
        name = self.children[0]
        parameters = self.children[1]
        
      #  print("function call debugging")
      #  print("Name: " , name)
      #  print("Params: " , parameters)
      #  print("ST: " ,symbol_table.declared_variables , symbol_table.functions[name])        
        
        #for param in parameters:
         # print("Param : " , param , type(param))
      
      
        if parameters == None and symbol_table.functions[name][0] != None:
            raise Exception()
        if parameters != None and symbol_table.functions[name][0] == None:
            raise Exception()
        
        arg_types = []
        for args in symbol_table.functions[name]:
            if args!= None:
                for arg in args:
                    arg_types.append(arg)
     
        
        
        arg_entry = ""
        call_label = symbol_table.get_unique_label(f'function_call_to_{name}')
        jump_label = f"_{name}__function"
        
        compiled_code.append([f"# Compiling Call to {name}" ])
        print("param length : " , len(parameters))
        for i in range(0,len(parameters)+1):
            #does type matter???
            pushentry = symbol_table.get_entry(PrimitiveType.NUMBR)
            symbol_table.push_call_stack(pushentry)
            compiled_code.append([f"PUSH {pushentry}"])                              
                              
        compiled_code.append(["PUSH" , call_label])
        

        
        #iterate over arguments and push them to stack
        if parameters != None:
            for i,arguments in enumerate(parameters):
                if arguments != None:
                 #   print("debugging function call: \n" , arguments , type(arguments), "\n")
                    if isinstance(arguments, NumbrLiteral) or isinstance(arguments, YarnLiteral) or isinstance(arguments,VariableUse) or isinstance(arguments, FunctionCall) or str(arguments)[-10:] == "Expression":
                        arg_entry = arguments.compile(symbol_table,compiled_code)
            
                        if isinstance(arguments, YarnLiteral) or isinstance(arguments, VariableUse):
                       #     print("Checking1: " , arg_types[i][1] , arg_entry.expr_type)
      
                            if arg_entry.expr_type != arg_types[i][1]:
                                raise Exception()
                        else:
                        #    print("Checking2: " , arg_types[i][1] , arguments.expr_type)

                            if arg_types[i][1] != arg_entry.expr_type:
                               raise Exception()
                    
                    
                    else:
                        if isinstance(arguments, list):
                            for argument in arguments:
                                if argument != None:
                                #    print(str(argument)[-10:])
                                    if str(argument)[-10:] == "Expression" or isinstance(argument, FunctionCall): 
                                        arg_entry = argument.compile(symbol_table,compiled_code)
                                        if arg_types[i][0][1] != arg_entry.expr_type:
                                            raise Exception()
                                    else:
                                        if arg_types[i][0][1] != arguments[0].expr_type:
                                            raise Exception()
                            
                                        value = str(argument)[15:len(str(argument)) - 1 ]
                                        arg_entry = symbol_table.get_entry(argument.expr_type)
                                        compiled_code.append(["VAL_COPY" , value, arg_entry])
                    #something going on with arg_entry here
                    compiled_code.append(["PUSH" , arg_entry])

#        print()
 #       print()
 #       print("reg we are trying to get : " , name)
 #       print("state of symbol table")
 #       print("current vars :" , symbol_table.declared_variables)
 #       print("current functions : " , symbol_table.functions)
 #       print("current returns : " , symbol_table.returns)
        temp = []
        if name in symbol_table.returns:
            for entry in symbol_table.returns:
                temp.append(entry)
            symbol_table.declared_variables[temp[0]] = temp[-1]

        guard_reg = symbol_table.get_entry_for_variable(name)
                 
                
        compiled_code.append(["JUMP" , jump_label ])
        compiled_code.append([f"{call_label}:"  ])
        
        for j in range(0,len(parameters)+1):
            popentry = symbol_table.pop_call_stack()
            compiled_code.append([f"POP {popentry}"])   
        
        compiled_code.append(["POP" , guard_reg])
       # PUSH function_call_to_function_zero_2 
       # JUMP _function_zero__function 
       # function_call_to_function_zero_2: 
       # POP s4 
        compiled_code.append([f"# Done Compiling Call to {name}" ])
       # print("guard reg? : " , guard_reg)
       
       
      #  print("vars at time of function call : " , symbol_table.declared_variables)
     #   func_reg = symbol_table.get_entry_for_variable(name)

        return guard_reg
   

class Function(ASTNode):
    def __init__(self, children):
        super().__init__(children=children)

    def compile(self, symbol_table, compiled_code):
      #  for child in self.children:
      #     print("Function debug: " , type(child) , child)
        """
            children 
            0 func name
            1 arguments 
            2 code block
            3 type_declaration (for found value)
        
        """
        
     #   for item in self.children[1]:
      #      print("item: " , item)
        
        
        # I HAS A x ITS A NUMBER 
        
        
        
        
        
        
        symbol_table.functions[self.children[0]] = [self.children[1]]
        symbol_table.returns[self.children[0]] = self.children[3]

     #   symbol_table.declare_variable(self.children[0] , self.children[3])
#        symbol_table.declare_variable(self.children)
        code_block = [self.children[2]]
        temp = []
        if code_block:
            children_reprs = [repr(child) for child in code_block]
            for entry in children_reprs:
                break_up = entry.split(" ")
                for item in break_up:
                    temp.append(item)
         #   print(temp)
            if temp[0].find("Function") != -1 and temp[0].find("FunctionCall") != temp[0].find("Function"):
                raise Exception("please no nested functions")

    #    if temp[0].find("FunctionCall"):
    #        pushreg = symbol_table.get_entry(self.children[3])
    #        print("pushreg : " , pushreg)
    #        compiled_code.append([f"PUSH {pushreg}"])
        
        symbol_table.increment_scope()

        end_label = symbol_table.get_unique_label(f'end_of__{self.children[0]}__function')
        call_label = f'_{self.children[0]}__function:'
     
        compiled_code.append([f"# Start of function definition for {self.children[0]}"])
                              
        compiled_code.append(["JUMP", end_label])
        compiled_code.append([call_label])

        if self.children[1] != None:
            try:
                if len(self.children[1]) > 1:
                    for argument in reversed(self.children[1]):
                        if argument != None:
                            if isinstance(argument[0],list):
                                name , arg_type = argument[0][0],argument[0][1]
                            else:
                                name , arg_type = argument[0],argument[1]
                                
                            argument_added = symbol_table.declare_variable(name , arg_type)
                            compiled_code.append(["POP" , argument_added])
                else:
                     for argument in self.children[1]:
                        if argument != None:
                            if isinstance(argument[0],list):
                                name , arg_type = argument[0][0],argument[0][1]
                            else:
                                name , arg_type = argument[0],argument[1]
                                
                            argument_added = symbol_table.declare_variable(name , arg_type)
                            compiled_code.append(["POP" , argument_added])
            except:
                for argument in self.children[1]:
                        if argument != None:
                            if isinstance(argument[0],list):
                                name , arg_type = argument[0][0],argument[0][1]
                            else:
                                name , arg_type = argument[0],argument[1]
                                
                            argument_added = symbol_table.declare_variable(name , arg_type)
                            compiled_code.append(["POP" , argument_added])
                            
                            
#        print(symbol_table.declared_variables)
#        print()        
#        print("children1: " , self.children[1][0])
     #   print("children2: ", self.children[2])
        
#        print()
      #  arg_check = symbol_table.get_entry_for_variable(self.children[1][0][0])
#        print(arg_check)
        self.children[2].compile(symbol_table,compiled_code)
        
      #  return_type = self.children[3]
     #   print(return_type)
        
        compiled_code.append([f"{end_label}:"])
        compiled_code.append([f"# End of function definition for {self.children[0]}"])
      #  print("relevant: " , self.children[0] , self.children[3])
   #     print("vars in func : " , symbol_table.declared_variables)

        symbol_table.decrement_scope()
        return_reg = symbol_table.declare_variable(self.children[0], self.children[3])
        
     #   print("testt" , symbol_table.declared_variables)
   #     print("vars outside func : " , symbol_table.declared_variables)
    #    print(return_reg.expr_type)
    #    print(symbol_table.declared_)
        return  return_reg
        
class Found(ASTNode):
    """
    Represents a block of statements. 
    For instance, the main program or part of a 
    flow control statement. Its children are a list
    of statements.
    """
    def __init__(self, children):
        super().__init__(children=children)

    def compile(self, symbol_table, compiled_code):
        compiled_code.append(["# Compiling Found Statement"])
      #  print("found children: " , self.children

        for child in self.children:
            print("Found children : " , child , type(child))                       
        return_reg = self.children[0].compile(symbol_table, compiled_code)
        
        for entry in(symbol_table.functions.items()):
            key = entry[0]
            if symbol_table.returns[key] != return_reg.expr_type:
                raise Exception()
        
        guard_reg = symbol_table.get_entry(PrimitiveType.NUMBR)
        
        compiled_code.append(["POP" , guard_reg])
        compiled_code.append(["PUSH" , return_reg])
        compiled_code.append(["JUMP" , guard_reg])
        
        
        
        symbol_table.returns[return_reg] = return_reg.expr_type
        return return_reg
        
    
########################################################################

        
        
class CodeBlock(ASTNode):
    """
    Represents a block of statements. 
    For instance, the main program or part of a 
    flow control statement. Its children are a list
    of statements.
    """
    def __init__(self, children):
        super().__init__(children=children)

    def compile(self, symbol_table, compiled_code):
        symbol_table.increment_scope()
        super().compile(symbol_table, compiled_code)
        symbol_table.decrement_scope()

class MainProgram(CodeBlock):
    """
    Represents the entire program, has a CodeBlock as
    its only child, and a version
    """
    def __init__(self, children, version):
        super().__init__(children=children)
        assert version.value == '1.450', version

    def compile(self, symbol_table, compiled_code):
        self.children[0].compile(symbol_table, compiled_code)

class PrimitiveLiteral(ASTNode):
    """
    An abstract base class that represents primitive literals
    The string of the value is stored as its only child.
    """
    def __init__(self, data, expr_type):
        super().__init__(children=[data])
        self.expr_type = expr_type

    def compile(self, symbol_table, compiled_code):
        entry = symbol_table.get_entry(expr_type=self.expr_type)
        compiled_code.append(['VAL_COPY', self.children[0], entry])
        return entry

class NumbrLiteral(PrimitiveLiteral):
    """
    An expression that represents a Numbr (like 5).
    The string of the value is stored as its only child.
    """
    def __init__(self, data):
        PrimitiveLiteral.__init__(self, data=data, expr_type=PrimitiveType.NUMBR)

class TroofLiteral(PrimitiveLiteral):
    """
    An expression that represents a Troof (like WIN).
    The string of the value is stored as its only child.
    Note the enclosing quotes are included in the string.
    """
    def __init__(self, data):
        PrimitiveLiteral.__init__(self, data=data, expr_type=PrimitiveType.TROOF)

    def compile(self, symbol_table, compiled_code):
        entry = symbol_table.get_entry(expr_type=self.expr_type)
        value = 1 if self.children[0] == 'WIN' else 0
        compiled_code.append(['VAL_COPY', value, entry])
        return entry

class LettrLiteral(PrimitiveLiteral):
    """
    An expression that represents a Lettr (like 'a').
    The string of the value is stored as its only child.
    Note the enclosing quotes are included in the string.
    """
    def __init__(self, data):
        PrimitiveLiteral.__init__(self, data=data, expr_type=PrimitiveType.LETTR)
    
    def compile(self, symbol_table, compiled_code):
        entry = symbol_table.get_entry(expr_type=self.expr_type)
        lettr = self.children[0] # like ':)'
        mapping_to_lmao_char = {
            "':)'": r"'\n'",
            "':>'": r"'\t'",
            "':''": r"'\''",
            "'::'": r"':'", 
            r"'\'": r"'\\'", 
        } 
        lmao_char = mapping_to_lmao_char.get(lettr, lettr)
        compiled_code.append(['VAL_COPY', lmao_char, entry])
        return entry

class VisibleStatement(ASTNode):
    """
    A statement generated from "VISIBLE <expr>, <expr>, <expr>".
    The expr node is stored as its only child.
    """
    def __init__(self, children, output_newline=True):
        super().__init__(children=children)
        self.output_newline = output_newline

    def compile(self, symbol_table, compiled_code):
        def print_entry(entry, compiled_code):
   
            
            if entry.expr_type in {PrimitiveType.NUMBAR, PrimitiveType.NUMBR, PrimitiveType.TROOF}:
                compiled_code.append(['OUT_NUM', entry])
            elif entry.expr_type == PrimitiveType.LETTR:
                compiled_code.append(['OUT_CHAR', entry])
     #   print("visible debug:" , self.children)
        for child in self.children:
            child_entry = child.compile(symbol_table, compiled_code)
            if isinstance(child_entry.expr_type, PrimitiveType):
                print_entry(child_entry, compiled_code)
            elif isinstance(child_entry.expr_type, ArrayType):
                compiled_code.append(['# Printing Array', child_entry])
                size_entry = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)
                compiled_code.append(['AR_GET_SIZE', child_entry, size_entry])
                index_entry = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)
                compiled_code.append(['VAL_COPY', 0, index_entry])
                
                loop_start = symbol_table.get_unique_label('visible_array_loop_start')
                compiled_code.append([loop_start + ':'])
                test_entry = symbol_table.get_entry(expr_type=PrimitiveType.TROOF)
                compiled_code.append(['TEST_GTE', index_entry, size_entry, test_entry])

                loop_end = symbol_table.get_unique_label('visible_array_loop_end')
                compiled_code.append(['JUMP_IF_N0', test_entry, loop_end])

                subtype = child_entry.expr_type.subtype
                value_entry = symbol_table.get_entry(expr_type=subtype)
                compiled_code.append(['AR_GET_IDX', child_entry, index_entry, value_entry])

                print_entry(value_entry, compiled_code)

                compiled_code.append(['ADD', 1, index_entry, index_entry])
                compiled_code.append(['JUMP', loop_start])
                compiled_code.append([loop_end + ':'])

                compiled_code.append(['# Done Printing Array', child_entry])
            else:
                raise CompilerTypeError(f'Unable to print type {child_entry.expr_type}')

        if self.output_newline:
            compiled_code.append(['OUT_CHAR', r"'\n'"])

class VariableDeclaration(ASTNode):
    """
    An expression that represents a varible identifier (like x).
    The string of the variable's name and its type are its children.
    """
    def compile(self, symbol_table, compiled_code):
        name, declaration_type  = self.children

       # print("Variables at VarDec: " , symbol_table.declared_variables)

        return symbol_table.declare_variable(name, declaration_type)

class VariableUse(ASTNode):
    """
    An expression that represents a varible identifier (like x).
    The string of the variable's name is stored as its only child.
    """
    def compile(self, symbol_table, compiled_code):
        name = self.children[0]
   #     print("compile order test")
        return symbol_table.get_entry_for_variable(name)

class MathBinaryExpression(ASTNode):
    """
    An expression that represents a math binary operation 
    (like 'SUM OF josh AN 6'). The children consist of
    the operator as a string (like 'SUM'), the first operand,
    and the second operand.
    """
    def compile(self, symbol_table, compiled_code):
        operator, expr_1, expr_2 = self.children
        entry_1 = expr_1.compile(symbol_table, compiled_code)
        entry_2 = expr_2.compile(symbol_table, compiled_code)

        numeric_types = {PrimitiveType.NUMBR, PrimitiveType.NUMBAR}
        if entry_1.expr_type not in numeric_types:
            raise CompilerTypeError(f'{expr_1} is not a numeric type.')
        if entry_2.expr_type not in numeric_types:
            raise CompilerTypeError(f'{expr_1} is not a numeric type.')
        if entry_1.expr_type != entry_2.expr_type:
            raise CompilerTypeError(f'{expr_1} and {expr_2} do not match types.')

        result_entry = symbol_table.get_entry(expr_type=entry_1.expr_type)
        
        math_lol_to_lmao = {
            'SUM': 'ADD',
            'DIFF': 'SUB',
            'PRODUKT': 'MULT',
            'QUOSHUNT': 'DIV',
        }
        lmao_command = math_lol_to_lmao[operator]
        compiled_code.append([lmao_command, entry_1, entry_2, result_entry])

     #   print("Variables at MathExpression: " , symbol_table.declared_variables)

        return result_entry

class MathUnaryExpression(ASTNode):
    """
    An expression that represents a math unary operation 
    (like 'FLIP OF 6'). The children consist of
    the operator as a string (like 'FLIP') and the operand.
    """
    def compile(self, symbol_table, compiled_code):
        operator, expr = self.children
        entry = expr.compile(symbol_table, compiled_code)

        numeric_types = {PrimitiveType.NUMBR, PrimitiveType.NUMBAR}
        if entry.expr_type not in numeric_types:
            raise CompilerTypeError(f'{entry} is not a numeric type.')

        result_entry = symbol_table.get_entry(expr_type=entry.expr_type)
        
        if operator == 'FLIP':
            compiled_code.append(['DIV', 1, entry, result_entry])
        else: # operator == 'SQUAR':
            compiled_code.append(['MULT', entry, entry, result_entry])
        return result_entry


class AssignmentExpression(ASTNode):
    """
    An expression that represents an assignment (like 'toyz R "us"')
    or intializations (like 'I HAS A x ITZ A NUMBR AN ITZ 5').
    Its expr_type is the type of the right side of the assignment
    (YARN and NUMBR in the above examples).
    The left side (the variable expression) and the right side (the value)
    being assigned compose its two children
    """
    def __init__(self, left_side, right_side):
        super().__init__(children=[left_side, right_side])
        
    
    def compile(self, symbol_table, compiled_code):
        
     #   print("Assignment check : " , symbol_table.declared_variables)


        left_side, right_side = self.children
        right_entry = right_side.compile(symbol_table, compiled_code)
        left_entry = left_side.compile(symbol_table, compiled_code)
        
#        print("right entry : " , right_side, type(right_side))

        
        if left_entry.expr_type != right_entry.expr_type:
            raise CompilerTypeError(f'{left_entry.expr_type} != {right_entry.expr_type}')
        if left_entry.array_entry:
            compiled_code.append(['AR_SET_IDX', left_entry.array_entry, 
                                  left_entry.index_entry, right_entry])
            compiled_code.append(['VAL_COPY', right_entry, left_entry])                     
        elif isinstance(left_entry.expr_type, PrimitiveType):
            compiled_code.append(['VAL_COPY', right_entry, left_entry])
        else:
            compiled_code.append(['AR_COPY', right_entry, left_entry])
        return left_entry

class LogicalExpressionLazy(ASTNode):
    """
    An expression that represents a logical expression 
    (like 'BOTH OF WIN AN FAIL').
    The first child is the operator, and the rest of the children
    are the TROOF expressions to be evaluated.
    Only evaluates as many operands as needed to determine result.
    """
    def compile(self, symbol_table, compiled_code):
        def check_is_troof_and_get_entry(expr):
            entry = expr.compile(symbol_table, compiled_code)
            if entry.expr_type != PrimitiveType.TROOF:
                raise CompilerTypeError(
                    f'Using non-TROOF type {entry.expr_type} in logical expression')
            return entry

        operator = self.children[0]
        
        result_entry = symbol_table.get_entry(expr_type=PrimitiveType.TROOF)
        child_exprs = self.children[1:]

        compiled_code.append([f'# Logical Expression (result in {result_entry})'])
        
        if operator == 'NOT':
            entry = check_is_troof_and_get_entry(child_exprs[0])
            compiled_code.append(['TEST_EQU', entry, 0, result_entry])
        elif operator in {'BOTH', 'ALL', 'EITHER', 'ANY'}:
            lazy_jump_label = symbol_table.get_unique_label(root='logical_lazy_jump')
            for expr in child_exprs:
                entry = check_is_troof_and_get_entry(expr)
                command = 'JUMP_IF_0' if operator in {'BOTH', 'ALL'} else 'JUMP_IF_N0'
                compiled_code.append([command, entry, lazy_jump_label])
            compiled_code.append(['VAL_COPY', entry, result_entry])

            end_label = symbol_table.get_unique_label(root='logical_end')
            compiled_code.append(['JUMP', end_label])
            compiled_code.append([lazy_jump_label + ':'])
            value = 0 if operator in {'BOTH', 'ALL'} else 1
            compiled_code.append(['VAL_COPY', value, result_entry])
            compiled_code.append([end_label + ':'])
        elif operator in {}:
            pass
        else: # operator == 'WON'
            entry_1 = check_is_troof_and_get_entry(child_exprs[0])
            entry_2 = check_is_troof_and_get_entry(child_exprs[1])
            compiled_code.append(['TEST_NEQU', entry_1, entry_2, result_entry])

        compiled_code.append([f'# Logical Expression (result in {result_entry}) Done'])
        return result_entry

class LogicalExpression(ASTNode):
    """
    An expression that represents a logical expression 
    (like 'BOTH OF WIN AN FAIL').
    The first child is the operator, and the rest of the children
    are the TROOF expressions to be evaluated.
    """
    def compile(self, symbol_table, compiled_code):
        operator = self.children[0]
        entries = [expr.compile(symbol_table, compiled_code) 
            for expr in self.children[1:]]
        result_entry = symbol_table.get_entry(expr_type=PrimitiveType.TROOF)
        if operator == 'NOT':
            compiled_code.append(['TEST_EQU', entries[0], 0, result_entry])
        elif operator in {'BOTH', 'EITHER', 'WON'}:
            compiled_code.append(['ADD', entries[0], entries[1], result_entry])
            if operator == 'BOTH': 
                compiled_code.append(['TEST_EQU', result_entry, 2, result_entry])
            elif operator == 'EITHER': 
                compiled_code.append(['TEST_GTE', result_entry, 1, result_entry])
            else: # operator == 'WON': 
                compiled_code.append(['TEST_EQU', result_entry, 1, result_entry])
        else: # operator in {'ALL', 'ANY'}:
            compiled_code.append(['VAL_COPY', 0, result_entry])
            for entry in entries:
                compiled_code.append(['ADD', entry, result_entry, result_entry])
            if operator == 'ALL':
                compiled_code.append(['TEST_EQU', len(entries), result_entry, result_entry])
            else: # operator == 'ANY'
                compiled_code.append(['TEST_GTE', result_entry, 1, result_entry])
        return result_entry



class ComparisonExpression(ASTNode):
    """
    An expression that represents a comparison expression 
    (like 'BOTH SAEM 5 AN 7').
    The first child is the operator, and the rest of the children
    are the two operands.
    """
    def compile(self, symbol_table, compiled_code):
        operator, expr_1, expr_2 = self.children
        entry_1 = expr_1.compile(symbol_table, compiled_code)
        entry_2 = expr_2.compile(symbol_table, compiled_code)
        result_entry = symbol_table.get_entry(expr_type=PrimitiveType.TROOF)
        
        if entry_1.expr_type != entry_2.expr_type:
            compiled_code.append(['VAL_COPY', 0, result_entry])
            return result_entry

        lol_to_lmao = {
            'SAEM': 'TEST_EQU',
            'DIFFRINT': 'TEST_NEQU',
            'FURSTSMALLR': 'TEST_LESS',
            'FURSTBIGGR': 'TEST_GTR',
        }
        lmao_command = lol_to_lmao[operator]
        compiled_code.append([lmao_command, entry_1, entry_2, result_entry])
        return result_entry


class WhatevrExpression(ASTNode):
    """
    A node representing a random NUMBR.
    """
    def __init__(self):
        super().__init__()
    
    def compile(self, symbol_table, compiled_code):
        result_entry = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)
        compiled_code.append(['RANDOM', result_entry])
        return result_entry

class GimmehExpression(ASTNode):
    """
    A node representing a request of a LETTR from standard input.
    """
    def __init__(self):
        super().__init__()
    
    def compile(self, symbol_table, compiled_code):
        result_entry = symbol_table.get_entry(expr_type=PrimitiveType.LETTR)
        compiled_code.append(['IN_CHAR', result_entry])
        return result_entry

class ORLYStatement(ASTNode):
    """
    A node representing a O RLY? statement.
    Its children are (in the following order):
        a conditional expression,
        a code block (YA RLY),
        a code block (possibly None) of NO WAI

    """
    def __init__(self, children):
        super().__init__(children=children)
    
    def compile(self, symbol_table, compiled_code):
        def compile_and_check_troof(expr):
            entry = expr.compile(symbol_table, compiled_code)
            if entry.expr_type != PrimitiveType.TROOF:
                raise CompilerTypeError(
                    f'{cond_entry.expr_type} is not an acceptable conditional expression')
            return entry

    #    print("if children : " , self.children)
     #   if self.children == None:
      #      raise Exception("failed if statement???")
    
        code_block = self.children
        temp = []
        if code_block:
            children_reprs = [repr(child) for child in code_block]
           # print("chld rp " , children_reprs)
            for entry in children_reprs:
                break_up = entry.split(" ")
                for item in break_up:
                    temp.append(item)
            if temp[1].find("Function") != -1:
                raise Exception("please no nested functions")



        compiled_code.append(['# Compiling O RLY Statement'])
        expr, if_true_block, otherwise_block = self.children
        
        oic_label = symbol_table.get_unique_label(root='oic')
        
        expr_entry = compile_and_check_troof(expr)
        after_label = symbol_table.get_unique_label(root='after_if_true_block')
        compiled_code.append(['JUMP_IF_0', expr_entry, after_label])
        if_true_block.compile(symbol_table, compiled_code)
        compiled_code.append(['JUMP', oic_label])
        compiled_code.append([after_label + ':'])


        if otherwise_block:
            otherwise_block.compile(symbol_table, compiled_code)

        compiled_code.append([oic_label + ':'])
        compiled_code.append(['# Done with O RLY Statement'])

class LoopStatement(ASTNode):
    """
    A node representing a loop statement.
    Its children are (in the following order):
        a code block representing the body of the loop
    """
    def compile(self, symbol_table, compiled_code):
        def compile_and_check_troof(expr):
            entry = expr.compile(symbol_table, compiled_code)
            if entry.expr_type != PrimitiveType.TROOF:
                raise CompilerTypeError(
                    f'{cond_entry.expr_type} is not an acceptable conditional expression')
            return entry

        compiled_code.append(['# Compiling Loop Statement'])
        assign_expression, til_expression, body = self.children

        start_label = symbol_table.get_unique_label(root='loop_start')
        compiled_code.append([start_label + ':'])

        end_label = symbol_table.get_unique_label(root='loop_end')

        if til_expression is not None:
            til_entry = compile_and_check_troof(til_expression)
            compiled_code.append(['JUMP_IF_N0', til_entry, end_label])

        symbol_table.push_GTFO_stack(end_label)

        body.compile(symbol_table, compiled_code)

        if assign_expression is not None:
            assign_expression.compile(symbol_table, compiled_code)

        compiled_code.append(['JUMP', start_label])
        compiled_code.append([end_label + ':'])
        symbol_table.pop_GTFO_stack()
        compiled_code.append(['# Done with Loop Statement'])

class GTFOStatement(ASTNode):
    """
    A node representing a GTFO (break) statement.
    It has no children. It relies on the Symbol Table to determine
    jump destination.
    """
    def compile(self, symbol_table, compiled_code):
        destination = symbol_table.read_GTFO_stack()
        compiled_code.append(['JUMP', destination])

class YarnLiteral(ASTNode):
    """
    An expression that represents a YARN (LOTZ OF LETTRs).
    It's only child is a string (with enclosing double quotes).
    """
    def compile(self, symbol_table, compiled_code):
        value = self.children[0]
        expr_type = ArrayType(PrimitiveType.LETTR)
        array_entry = symbol_table.get_entry(expr_type=expr_type)
        compiled_code.append(['# Compiling YARN', value, array_entry])

        letters = []
        value = value[1:-1] # remove enclosing double quotes
        while value:
            first_letter = value[0]
            if first_letter == ':':
                escaped_letter = value[1]
                mapping_to_lmao_char = {
                    ")": r"'\n'",
                    ">": r"'\t'",
                    '"': '\'"\'',
                    ":": r"':'", 
                } 
                value = value[2:]
                letters.append(mapping_to_lmao_char[escaped_letter])
            else: 
                if first_letter == "'":
                    letter = r'\''
                else:
                    letter = first_letter
                letters.append("'" + letter + "'")
                value = value[1:]
        compiled_code.append(['# LMAO chars', letters])
        compiled_code.append(['AR_SET_SIZE', array_entry, len(letters)])
        for i, letter in enumerate(letters):
            compiled_code.append(['AR_SET_IDX', array_entry, i, letter])
        compiled_code.append(['# Done compiling YARN'])
        return array_entry

class ArrayDeclaration(ASTNode):
    """
    A node representing an array declaration. Its children are its name,
    the type of the array, and its size (as an expression).
    """
    def compile(self, symbol_table, compiled_code):
        name, array_type, size_expr = self.children
        array_entry = symbol_table.declare_variable(name, array_type)
        size_entry = size_expr.compile(symbol_table, compiled_code)
        if size_entry.expr_type != PrimitiveType.NUMBR:
            raise CompilerTypeError(f'{size_entry.expr_type} is not accceptable size for array')
        compiled_code.append(['AR_SET_SIZE', array_entry, size_entry])

class ArrayIndex(ASTNode):
    """
    A node representing an array index (like "x'Z 0"). It has two children,
    an VariableUse node and an index expression.
    """
    def compile(self, symbol_table, compiled_code):
        array_node, index_expr = self.children
        array_entry = array_node.compile(symbol_table, compiled_code)
        index_entry = index_expr.compile(symbol_table, compiled_code)
        if index_entry.expr_type != PrimitiveType.NUMBR:
            raise CompilerTypeError(f'{index_entry.expr_type} is not accceptable size for array')
        
        array_subtype = array_entry.expr_type.subtype
        result_entry = symbol_table.get_array_index_entry(
            expr_type=array_subtype, array_entry=array_entry, index_entry=index_entry)
        
        compiled_code.append(['AR_GET_IDX', array_entry, index_entry, result_entry])
        return result_entry

class LengthzExpression(ASTNode):
    """
    A node representing an lengthz expression, its only child is the array expression.
    """
    def compile(self, symbol_table, compiled_code):
        expr = self.children[0]
        array_entry = expr.compile(symbol_table, compiled_code)
        if not isinstance(array_entry.expr_type, ArrayType):
            raise CompilerTypeError(f'Can not get length of non-array type {array_entry.expr_type}')
        result_entry = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)
        compiled_code.append(['AR_GET_SIZE', array_entry, result_entry])
        return result_entry

class CaseStatement(ASTNode):
    """
    A node representing a case (WTF?) statement.
    Its children are (in the following order):
        an expression to be matched with the cases,
        a (possibly empty list of cases).
    Cases with two elements consist of a literal and a block.
    A last case with a single element is the default block.

    """
    def compile(self, symbol_table, compiled_code):
        compiled_code.append(['# Case Statement'])
        expr, cases = self.children

        expr_entry = expr.compile(symbol_table, compiled_code)

        literals = []
        blocks = []
        block_labels = []
        for case in cases:
            if len(case) == 2:
                literal, block = case
                literals.append(literal)
            else:
                block = case[0]
            blocks.append(block)
            block_labels.append(symbol_table.get_unique_label(root='block_start'))
        
        for literal, block_label in zip(literals, block_labels):
            literal_entry = literal.compile(symbol_table, compiled_code)

            if literal_entry.expr_type != expr_entry.expr_type:
                raise CompilerTypeError(f'Type mismatch in case statement')

            test_entry = symbol_table.get_entry(expr_type=PrimitiveType.TROOF)

            if isinstance(literal_entry.expr_type, PrimitiveType):
                compiled_code.append(['TEST_EQU', expr_entry, literal_entry, test_entry])
            else:
                index = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)
                literal_size = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)
                expr_size = symbol_table.get_entry(expr_type=PrimitiveType.NUMBR)

                literal_element = symbol_table.get_entry(expr_type=literal_entry.expr_type.subtype)
                expr_element = symbol_table.get_entry(expr_type=literal_entry.expr_type.subtype)

                equal_array_start = symbol_table.get_unique_label(root='equal_array_start')
                equal_array_end = symbol_table.get_unique_label(root='equal_array_end')
                compiled_code += [
                    ['# Doing array equality test for case statement'],
                    ['AR_GET_SIZE', literal_entry, literal_size],
                    ['AR_GET_SIZE', expr_entry, expr_size],
                    ['TEST_EQU', literal_size, expr_size, test_entry],
                    ['JUMP_IF_0', test_entry, equal_array_end, '# Jump if different sizes'],

                    ['# Check all indices'],
                    ['VAL_COPY', 0, index],
                    [equal_array_start + ':'],

                    ['TEST_GTE', index, literal_size, test_entry],
                    ['JUMP_IF_N0', test_entry, equal_array_end, '# Reached end of array with no mismatches'],

                    ['AR_GET_IDX', literal_entry, index, literal_element],
                    ['AR_GET_IDX', expr_entry, index, expr_element],
                    ['TEST_EQU', literal_element, expr_element, test_entry],
                    ['JUMP_IF_0', test_entry, equal_array_end],
                    ['ADD', 1, index, index],
                    ['JUMP', equal_array_start],
                    [equal_array_end + ':']
                ]
            compiled_code.append(['JUMP_IF_N0', test_entry, block_label])
        
        if len(block_labels) > len(literals): # default provided
            compiled_code.append(['JUMP', block_labels[-1]])
        
        end_label = symbol_table.get_unique_label(root='case_end')
        compiled_code.append(['JUMP', end_label])
             
        symbol_table.push_GTFO_stack(end_label)

        for block_label, block in zip(block_labels, blocks):
            compiled_code.append([block_label + ':'])
            block.compile(symbol_table, compiled_code)


        symbol_table.pop_GTFO_stack()
        compiled_code.append([end_label + ':'])

        