# I'm importing pytest so I can write and run tests
import pytest

# I'm importing the rule-based functions from my app
from app import (
    rule_based_quadratic_method,
    rule_based_simultaneous_method,
    rule_based_ratio_method,
    rule_based_gp_method,
    rule_based_ap_method,
)


# ==================================================
# UNIT TEST: QUADRATIC METHOD
# ==================================================
# I'm checking that a factorisable quadratic recommends Factorisation
def test_rule_based_quadratic_method_factorisation():
    method, explanation = rule_based_quadratic_method(1, 5, 6)

    assert method == "Factorisation"
    assert "factorised" in explanation.lower() or "factorisation" in explanation.lower()


# ==================================================
# UNIT TEST: SIMULTANEOUS METHOD
# ==================================================
# I'm checking that easy matching coefficients recommend Elimination
def test_rule_based_simultaneous_method_elimination():
    method, explanation, eq1, eq2 = rule_based_simultaneous_method(2, 3, 7, 2, -1, 5)

    assert method == "Elimination"
    assert "elimination" in explanation.lower()


# ==================================================
# UNIT TEST: RATIO METHOD
# ==================================================
# I'm checking that ratio questions return the expected combined recommendation
def test_rule_based_ratio_method():
    method, explanation = rule_based_ratio_method(60, 2, 3)

    assert method == "Unitary Method or Fraction Method"
    assert "unitary" in explanation.lower()
    assert "fraction" in explanation.lower()


# ==================================================
# UNIT TEST: GP METHOD
# ==================================================
# I'm checking that if r is missing, Formula Method is recommended
def test_rule_based_gp_method_formula():
    method, explanation = rule_based_gp_method(None, 3, None, 5)

    assert method == "Formula Method"
    assert "formula" in explanation.lower()


# ==================================================
# UNIT TEST: AP METHOD
# ==================================================
# I'm checking that if d is known and nth term is missing, Iteration Method is recommended
def test_rule_based_ap_method_iteration():
    method, explanation = rule_based_ap_method(None, 4, 3, 6)

    assert method == "Iteration Method"
    assert "iteration" in explanation.lower()