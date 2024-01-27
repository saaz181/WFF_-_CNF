import re

class WFFChecker:
    @staticmethod
    def check_wff_rules(expr_str):
        # Rule 1: (P) is not a valid WFF.
        if re.match(r'^\(\s*[^\s()]+\s*\)$', expr_str):
            return False

        # Rule 2: ¬P ∧ Q can be either (¬P∧Q) or ¬(P∧Q), so it is not a valid WFF.
        if re.search(r'\b¬[^\s()]+\s*∧\s*[^\s()]+\b', expr_str):
            return False

        # Rule 3: ((P ⇒ Q)) is not a valid WFF due to unnecessary outer parentheses.
        if re.match(r'^\(\(\s*[^\s()]+\s*⇒\s*[^\s()]+\s*\)\)$', expr_str):
            return False

        # Rule 4: (P ⇒⇒ Q) is not a valid WFF due to a connective symbol right after a connective symbol.
        if re.search(r'[^\s()]⇒⇒[^\s()]', expr_str):
            return False

        # Rule 5: ((P ∧ Q) ∧)Q) is not a valid WFF due to the invalid placement of conjunction operator.
        if re.search(r'\(\(\s*[^\s()]+\s*∧\s*[^\s()]+\s*\)\s*∧\s*\)\s*[^\s()]+\s*\)', expr_str):
            return False

        # Rule 6: ((P ∧ Q) ∧ PQ) is not a valid WFF due to the invalid placement of variables.
        if re.search(r'\(\(\s*[^\s()]+\s*∧\s*[^\s()]+\s*\)\s*∧\s*[^\s()]+\s*[^\s()]+\s*\)', expr_str):
            return False

        # Rule 7: (P ∨ Q) ⇒ (∧ Q) is not a valid WFF due to insufficient variables for the conjunction component.
        if re.search(r'\(\s*[^\s()]+\s*∨\s*[^\s()]+\s*⇒\s*\(\s*∧\s*[^\s()]+\s*\)\s*\)', expr_str):
            return False

        # Additional rule: \lnot P \lnot Q is the same as PQ, and is not valid.
        if re.search(r'\b¬[^\s()]+\s*¬[^\s()]+\b', expr_str):
            return False

        # If none of the rules are violated, the expression is valid.
        return True

# Example usage:
# ¬ ∧ ⇒ ∨
expr_str = r"( ¬q ¬p ) ⇒ ∧ (¬p ∧ (r ⇒ q))"
is_valid_wff = WFFChecker.check_wff_rules(expr_str)
print(f"The given expression is a valid WFF: {is_valid_wff}")
