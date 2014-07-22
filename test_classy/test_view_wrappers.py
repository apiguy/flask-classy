from flask import Flask
from .view_classes import (BeforeRequestView, BeforeViewView, AfterRequestView, AfterViewView, DecoratedView,
                           BeforeRequestReturnsView, BeforeViewReturnsView, MakeResponseView)
from nose.tools import *

app = Flask("wrappers")
BeforeRequestView.register(app)
BeforeRequestReturnsView.register(app)
BeforeViewView.register(app)
BeforeViewReturnsView.register(app)
AfterViewView.register(app)
AfterRequestView.register(app)
DecoratedView.register(app)
MakeResponseView.register(app)

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


def test_before_request_returns():
    resp = client.get("/beforerequestreturns/")
    eq_(b"BEFORE", resp.data)

def test_before_view_returns():
    resp = client.get("/beforeviewreturns/")
    eq_(b"BEFORE", resp.data)

def test_make_response_view():
    resp = client.get("/makeresponse/")
    eq_(b"Make Response", resp.data)
