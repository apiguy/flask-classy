from flask import Flask
from .view_classes import BasicView, RouteBaseView
from nose.tools import *

app = Flask('route_base')
BasicView.register(app, route_base="/rb_test/")
BasicView.register(app)
RouteBaseView.register(app, route_base="/rb_test2/")
RouteBaseView.register(app)


def test_registered_route_base():
    client = app.test_client()
    resp = client.get('/rb_test/')
    eq_(b"Index", resp.data)


def test_no_route_base_after_register_route_base():
    client = app.test_client()
    resp = client.get('/basic/')
    eq_(b"Index", resp.data)


def test_route_base_override():
    client = app.test_client()
    resp = client.get('/rb_test2/')
    eq_(b"Index", resp.data)


def test_route_base_after_route_base_override():
    client = app.test_client()
    resp = client.get('/base-routed/')
    eq_(b"Index", resp.data)