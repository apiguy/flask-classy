from view_classes import VariedMethodsView
from nose.tools import *

def test_special_method_detected():
    members = [m[1] for m in VariedMethodsView.find_member_methods()]
    assert VariedMethodsView.index in members

def test_routed_method_detected():
    members = [m[1] for m in VariedMethodsView.find_member_methods()]
    assert VariedMethodsView.routed_method in members

def test_classmethod_ignored():
    members = [m[1] for m in VariedMethodsView.find_member_methods()]
    assert VariedMethodsView.class_method not in members
