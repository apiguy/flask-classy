from flask import Flask, url_for
from .view_classes import DecoratedView
from nose.tools import *

app = Flask("decorated")
DecoratedView.register(app)
client = app.test_client()


def test_func_decorator_index():
    resp = client.get('/decorated/')
    eq_(b"Index", resp.data)


def test_func_decorator_get():
    resp = client.get('/decorated/1234')
    eq_(b"Get 1234", resp.data)


def test_recursive_decorator_post():
    resp = client.post('/decorated/')
    eq_(b"Post", resp.data)


def test_more_recursive_decorator_get():
    resp = client.get('/decorated/get_some/')
    eq_(b"Get Some", resp.data)


def test_multiple_recursive_decorators_get():
    resp = client.get('/decorated/get_this/')
    eq_(b"Get This", resp.data)


def test_routes_with_recursive_decorators():
    resp = client.get('/decorated/mixitup/')
    eq_(b"Mix It Up", resp.data)


def test_recursive_with_parameter():
    resp = client.get('/decorated/someval/1234')
    eq_(b"Someval 1234", resp.data)


def test_recursive_with_route_with_parameter():
    resp = client.get('/decorated/anotherval/1234')
    eq_(b"Anotherval 1234", resp.data)


def test_params_decorator():
    resp = client.get('/decorated/params_decorator_method/')
    eq_(b"Params Decorator", resp.data)

def test_params_decorator_delete():
    resp = client.delete('/decorated/1234')
    eq_(b"Params Decorator Delete 1234", resp.data)



