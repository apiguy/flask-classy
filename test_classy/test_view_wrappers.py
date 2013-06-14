from flask import Flask
from .view_classes import BeforeRequestView, BeforeViewView, AfterRequestView, AfterViewView, DecoratedView
from nose.tools import *

app = Flask("wrappers")
BeforeRequestView.register(app)
BeforeViewView.register(app)
AfterViewView.register(app)
AfterRequestView.register(app)
DecoratedView.register(app)

client = app.test_client()

def test_before_request():
    resp = client.get("/beforerequest/")
    eq_(b"Before Request", resp.data)

def test_before_view():
    resp = client.get("/beforeview/")
    eq_(b"Before View", resp.data)

def test_after_view():
    resp = client.get("/afterview/")
    eq_(b"After View", resp.data)

def test_after_request():
    resp = client.get("/afterrequest/")
    eq_(b"After Request", resp.data)

def test_decorated_view():
    resp = client.get("/decorated/")
    eq_(b"Index", resp.data)

    resp = client.get("/decorated/1234")
    eq_(b"Get 1234", resp.data)
