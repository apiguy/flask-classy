from flask import Flask
from .view_classes import BasicView, TrailingSlashView, InheritedTrailingSlashView, OverrideInheritedTrailingSlashView
from nose.tools import *

app = Flask('trailing_slash')
BasicView.register(app, trailing_slash=False)
TrailingSlashView.register(app)
InheritedTrailingSlashView.register(app)
OverrideInheritedTrailingSlashView.register(app)

client = app.test_client()

def test_index():
    resp = client.get("/basic")
    eq_(b"Index", resp.data)

def test_get():
    resp = client.get("/basic/1234")
    eq_(b"Get 1234", resp.data)

def test_put():
    resp = client.put("/basic/1234")
    eq_(b"Put 1234", resp.data)

def test_patch():
    resp = client.patch("/basic/1234")
    eq_(b"Patch 1234", resp.data)

def test_post():
    resp = client.post("/basic")
    eq_(b"Post", resp.data)

def test_delete():
    resp = client.delete("/basic/1234")
    eq_(b"Delete 1234", resp.data)

def test_custom_method():
    resp = client.get("/basic/custom_method")
    eq_(b"Custom Method", resp.data)

def test_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    eq_(b"Custom Method 1234 abcd", resp.data)

def test_routed_method():
    resp = client.get("/basic/routed/")
    eq_(b"Routed Method", resp.data)


# TrailingSlashView

def test_trailing_index():
    resp = client.get("/trailing")
    eq_(b"Index", resp.data)
    
def test_trailing_get():
    resp = client.get("/trailing/1234")
    eq_(b"Get 1234", resp.data)

def test_trailing_put():
    resp = client.put("/trailing/1234")
    eq_(b"Put 1234", resp.data)

def test_trailing_patch():
    resp = client.patch("/trailing/1234")
    eq_(b"Patch 1234", resp.data)

def test_trailing_post():
    resp = client.post("/trailing")
    eq_(b"Post", resp.data)

def test_trailing_delete():
    resp = client.delete("/trailing/1234")
    eq_(b"Delete 1234", resp.data)

def test_trailing_custom_method():
    resp = client.get("/trailing/custom_method")
    eq_(b"Custom Method", resp.data)

def test_trailing_custom_method_with_params():
    resp = client.get("/trailing/custom_method_with_params/1234/abcd")
    eq_(b"Custom Method 1234 abcd", resp.data)

def test_trailing_routed_method():
    resp = client.get("/trailing/routed/")
    eq_(b"Routed Method", resp.data)

def test_trailing_routed_method2():
    resp = client.get("/trailing/routed2")
    eq_(b"Routed Method 2", resp.data)


# InheritedTrailingSlashView

def test_inherited_trailing_slash():
    resp = client.get("/inherited/trailing")
    eq_(b"Index", resp.data)


# OverrideInheritedTrailingSlashView

def test_inherited_trailing_slash_override():
    resp = client.get("/override/trailing/")
    eq_(b"Index", resp.data)

