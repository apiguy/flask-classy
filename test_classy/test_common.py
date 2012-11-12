from flask import Flask
from view_classes import BasicView
from nose.tools import *

app = Flask("common")
BasicView.register(app)

client = app.test_client()

def test_index():
    resp = client.get("/basic/")
    eq_("Index", resp.data)

def test_get():
    resp = client.get("/basic/1234/")
    eq_("Get 1234", resp.data)

def test_put():
    resp = client.put("/basic/1234/")
    eq_("Put 1234", resp.data)

def test_patch():
    resp = client.patch("/basic/1234/")
    eq_("Patch 1234", resp.data)

def test_post():
    resp = client.post("/basic/")
    eq_("Post", resp.data)

def test_delete():
    resp = client.delete("/basic/1234/")
    eq_("Delete 1234", resp.data)

def test_custom_method():
    resp = client.get("/basic/custom_method/")
    eq_("Custom Method", resp.data)

def test_routed_method():
    resp = client.get("/basic/routed/")
    eq_("Routed Method", resp.data)

def test_multi_routed_method():
    resp = client.get("/basic/route1/")
    eq_("Multi Routed Method", resp.data)

    resp = client.get("/basic/route2/")
    eq_("Multi Routed Method", resp.data)








