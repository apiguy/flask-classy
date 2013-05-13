from flask import Flask, url_for
from view_classes import DecoratedView
from nose.tools import *

app = Flask("decorated")
DecoratedView.register(app)
client = app.test_client()

def test_func_decorator_index():
	resp = client.get('/decorated/')
	eq_("Index", resp.data)

def test_func_decorator_get():
	resp = client.get('/decorated/1234')
	eq_("Get 1234", resp.data)