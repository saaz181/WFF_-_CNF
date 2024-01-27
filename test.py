from symbols import Expression

expr_str = """( \lnot q \lnot p ) \\rightarrow \wedge (\lnot p \wedge (r \\rightarrow q ))"""
test2 = "\lnot p"

expr_str2 = """\lnot (p \wedge \lnot q)"""

expr = Expression(expr_str)
print(expr.to_sympy())

# expr.paranthesis_check()
# expr.remove_extra_paranthesis()
# expr.token_check()
# expr.check_wff_rules()