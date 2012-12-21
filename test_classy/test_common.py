from flask import Flask, url_for
from view_classes import BasicView, IndexView
from nose.tools import *

app = Flask("common")
BasicView.register(app)
IndexView.register(app)

client = app.test_client()

def test_index():
    resp = client.get("/basic/")
    eq_("Index", resp.data)

def test_get():
    resp = client.get("/basic/1234")
    eq_("Get 1234", resp.data)

def test_put():
    resp = client.put("/basic/1234")
    eq_("Put 1234", resp.data)

def test_patch():
    resp = client.patch("/basic/1234")
    eq_("Patch 1234", resp.data)

def test_post():
    resp = client.post("/basic/")
    eq_("Post", resp.data)

def test_delete():
    resp = client.delete("/basic/1234")
    eq_("Delete 1234", resp.data)

def test_custom_method():
    resp = client.get("/basic/custom_method/")
    eq_("Custom Method", resp.data)

def test_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    eq_("Custom Method 1234 abcd", resp.data)

def test_routed_method():
    resp = client.get("/basic/routed/")
    eq_("Routed Method", resp.data)

def test_multi_routed_method():
    resp = client.get("/basic/route1/")
    eq_("Multi Routed Method", resp.data)

    resp = client.get("/basic/route2/")
    eq_("Multi Routed Method", resp.data)

def test_no_slash():
    resp = client.get("/basic/noslash")
    eq_("No Slash Method", resp.data)

def test_index_view_index():
    resp = client.get("/")
    eq_("Index", resp.data)

def test_custom_http_method():
    resp = client.post("/basic/route3/")
    eq_("Custom HTTP Method", resp.data)









