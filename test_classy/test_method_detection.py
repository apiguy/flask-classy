from flask_classy import get_interesting_members, FlaskView
from .view_classes import VariedMethodsView, SubVariedMethodsView
from nose.tools import *

def test_special_method_detected():
    members = [m[1] for m in get_interesting_members(FlaskView, VariedMethodsView)]
    assert VariedMethodsView.index in members

def test_routed_method_detected():
    members = [m[1] for m in get_interesting_members(FlaskView, VariedMethodsView)]
    assert VariedMethodsView.routed_method in members

def test_classmethod_ignored():
    members = [m[1] for m in get_interesting_members(FlaskView, VariedMethodsView)]
    assert VariedMethodsView.class_method not in members

def test_subclass_classmethod_ignored():
    members = [m[1] for m in get_interesting_members(FlaskView, SubVariedMethodsView)]
    assert SubVariedMethodsView.class_method not in members
    assert VariedMethodsView.class_method not in members
