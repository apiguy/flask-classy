from flask import Flask
from .view_classes import InheritanceView
from nose.tools import *

app = Flask('inheritance')
InheritanceView.register(app)

client = app.test_client()


def test_index():
    resp = client.get('/inheritance/')
    eq_(b"Index", resp.data)


def test_override():
    resp = client.get("/inheritance/1234/")
    eq_(b"Inheritance Get 1234", resp.data)

def test_inherited():
    resp = client.post('/inheritance/')
    eq_(b"Post", resp.data)

def test_with_route():
    resp = client.get("/inheritance/with_route")
    eq_(b"Inheritance with route", resp.data)


def test_override_with_route():
    resp = client.delete("/inheritance/1234/delete")
    eq_(b"Inheritance Delete 1234", resp.data)
