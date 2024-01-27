from enum import Enum
import string
import re
from sympy import sympify


class Operators(Enum):
    _and = '\wedge'
    _or = '\\vee'
    _then = '\\rightarrow'
    _not = '\lnot'



class Expression:
    def __init__(self, expr: str):
        self.expr: str = expr
        self.binary_operators = ['\wedge', '\\vee', '\\rightarrow']
        self.singular_operators = ['\lnot']
        self.operators = self.binary_operators + self.singular_operators
        self.paranthesis = ['(', ')']
        self.terms = [_char for _char in string.ascii_letters + string.whitespace]
        self.tokens = self.operators + self.paranthesis + self.terms

    
    def to_sympy(self):
        """
        Convert the logical expression to a SymPy expression.
        """
        sympy_expr = sympify(self.expr)
        return sympy_expr


    def convert_latex_to_sympy(self):
        print(self.expr_tokens)


    @staticmethod
    def string_replacement(_str: str, replacement: str, start_index: int, end_index: int) -> str:
        return _str[:start_index] + replacement + _str[end_index + 1:]

    def paranthesis_check(self) -> bool:
        stack: list(str, int) = []
        self.content_of_paranthesis: list(str, tuple) = []

        for index, _char in enumerate(self.expr):
            if _char == '(':
                stack.append((_char, index))
            
            elif _char == ')':
                # pop the element & get the `open_index`` from the stack
                _, open_index = stack.pop()

                # content inside paranthesis
                content_inside: str = self.expr[open_index: index + 1]

                # update the paranthesis array
                self.content_of_paranthesis.append([content_inside, (open_index, index)])

        
        return len(stack) == 0
    
    def remove_extra_paranthesis(self) -> bool:
        for item, (start_index, end_index) in self.content_of_paranthesis:

            carved_out_expr: str = item.replace('(', '').replace(')', '').strip()

            if len(carved_out_expr) == 1:
                self.expr = self.string_replacement(self.expr, carved_out_expr, start_index, end_index)


            if carved_out_expr.startswith('\lnot'):
                if len(carved_out_expr.split(' ')) == 2:
                    self.expr = self.string_replacement(self.expr, carved_out_expr, start_index, end_index - 2)

            # TODO: more to be implemented

    def token_check(self) -> bool | None:
        i = 0

        # tokenize the expr -> remove paranthesis
        self.expr_tokens = []
        
        while i < len(self.expr):
            if self.expr[i] == '\\':
                start_index_of_keyword = i

                while self.expr[i] != " ":
                    i += 1
                
                keyword = self.expr[start_index_of_keyword: i]
                if keyword not in self.tokens:
                    raise Exception(f"Token {keyword} is not Valid!")

                else:
                    self.expr_tokens.append(keyword.strip())

            else:
                if self.expr[i] not in self.tokens:
                    raise Exception(f"Token {self.expr[i]} is not Valid!")
                else:
                    if not self.expr[i].isspace() and self.expr[i] not in self.paranthesis:
                        self.expr_tokens.append(self.expr[i])
            i += 1

        return True        
    
    
    def is_not_consecutive_binary_operator(self):
        i = 0
        while i < len(self.expr_tokens) - 1:
            if self.expr_tokens[i] in self.binary_operators and \
                self.expr_tokens[i + 1] in self.binary_operators:
                raise Exception(f"Invalid Expression {self.expr_tokens[i]} - {self.expr_tokens[i+1]}")
            
            elif self.expr_tokens[i] in self.terms and \
                self.expr_tokens[i + 1] in self.terms:
                raise Exception(f"Two terms beside each other: {self.expr_tokens[i]} - {self.expr_tokensp[i + 1]}")



            i += 1

        return True


    
    def check_consecutive_terms(self):
        i = 0
        
        while i < len(self.expr_tokens):
            if self.expr_tokens[i] in self.singular_operators:
                if self.expr_tokens[i + 1] not in self.singular_operators + self.terms:
                    raise Exception(f"Invalid Expression -> {self.expr_tokens[i]} {self.expr_tokens[i + 1]}")


    def check_wff_rules(self):
        """
        Additional rules for WFF:
        1. (P) is not a valid WFF.
        2. ¬P ∧ Q can be either (¬P∧Q) or ¬(P∧Q), so it is not a valid WFF.
        3. ((P ⇒ Q)) is not a valid WFF due to unnecessary outer parentheses.
        4. (P ⇒⇒ Q) is not a valid WFF due to a connective symbol right after a connective symbol.
        5. ((P ∧ Q) ∧)Q) is not a valid WFF due to the invalid placement of conjunction operator.
        6. ((P ∧ Q) ∧ PQ) is not a valid WFF due to the invalid placement of variables.
        7. (P ∨ Q) ⇒ (∧ Q) is not a valid WFF due to insufficient variables for the conjunction component.
        """

        # Rule 1: (P) is not a valid WFF
        if len(self.expr_tokens) == 3 and self.expr_tokens[0] == '(' and self.expr_tokens[2] == ')':
            raise Exception("Invalid Expression: (P) is not a valid WFF.")

        # Rule 2: ¬P ∧ Q can be either (¬P∧Q) or ¬(P∧Q), so it is not a valid WFF.
        if '\lnot' in self.expr_tokens and '\wedge' in self.expr_tokens:
            not_index = self.expr_tokens.index('\lnot')
            and_index = self.expr_tokens.index('\wedge')
            if not_index < and_index:
                if not_index > 0 and and_index < len(self.expr_tokens) - 1:
                    raise Exception("Invalid Expression: ¬P ∧ Q is ambiguous without parentheses.")

        # Rule 3: ((P ⇒ Q)) is not a valid WFF due to unnecessary outer parentheses.
        if self.expr_tokens[0] == '(' and self.expr_tokens[-1] == ')':
            inner_expr = Expression(" ".join(self.expr_tokens[1:-1]))
            if inner_expr.token_check() and inner_expr.structure_check():
                raise Exception("Invalid Expression: Unnecessary outer parentheses.")

        # Rule 4: (P ⇒⇒ Q) is not a valid WFF due to a connective symbol right after a connective symbol.
        for i in range(len(self.expr_tokens) - 1):
            if self.expr_tokens[i] in self.binary_operators and self.expr_tokens[i + 1] in self.binary_operators:
                raise Exception(f"Invalid Expression: {self.expr_tokens[i]} {self.expr_tokens[i + 1]} is not allowed.")

        # Rule 5: ((P ∧ Q) ∧)Q) is not a valid WFF due to the invalid placement of conjunction operator.
        if '\wedge' in self.expr_tokens and ')' in self.expr_tokens:
            wedge_index = self.expr_tokens.index('\wedge')
            paren_index = self.expr_tokens.index(')')
            if wedge_index > paren_index:
                raise Exception("Invalid Expression: Invalid placement of conjunction operator.")

        # Rule 6: ((P ∧ Q) ∧ PQ) is not a valid WFF due to the invalid placement of variables.
        if '\wedge' in self.expr_tokens and any(term.isalpha() for term in self.expr_tokens):
            raise Exception("Invalid Expression: Invalid placement of variables.")

        # Rule 7: (P ∨ Q) ⇒ (∧ Q) is not a valid WFF due to insufficient variables for the conjunction component.
        if '\vee' in self.expr_tokens and '\wedge' in self.expr_tokens:
            or_index = self.expr_tokens.index('\vee')
            and_index = self.expr_tokens.index('\wedge')
            if len(set(self.expr_tokens[or_index + 1:and_index])) < 2:
                raise Exception("Invalid Expression: Insufficient variables for the conjunction component.")



    def structure_check(self):
        """
        1 - Check not two or more \\vee | \wedge | \lnot | \\rightarrow | alphabet is beside each other:
            For Example: 
                \lnot \lnot | \\vee \\vee || p p || \lnot p \lnot p are invalid cases
        
        2. \\vee | \wedge | \\rightarrow is combination 3 operation
            For Example:
                p \\vee q | p \\wedge q | p \\rightbarrow \lnot q are valid syntax. 
        
        3. \lnot should be treated as single character
            For Example:
                \lnot p -> single character
        """

        for token in self.expr_tokens:
            print(token)

        # First: Beside Check
        for opt in self.binary_operators:
            if not self.is_not_consecutive_binary_operator():
                print(f"Invalid: Two or more consecutive {opt} operators.")

        for opt in self.singular_operators:
            pass
            
        

        




        




