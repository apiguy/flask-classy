from flask import Flask, Blueprint
from .view_classes import BasicView, SubdomainAttributeView, SubdomainRouteView
from nose.tools import *

app = Flask("blueprints")
app.config["SERVER_NAME"] = "test.test"

bp = Blueprint("bptest1", "bptest2")
SubdomainAttributeView.register(bp)
SubdomainRouteView.register(bp)
BasicView.register(bp, subdomain="sub3")

bp2 = Blueprint("bptest2", "bptest2", subdomain="sub4")
BasicView.register(bp2)

app.register_blueprint(bp)
app.register_blueprint(bp2)

client = app.test_client()

def test_bp_attr_subdomain():
    resp = client.get("/subdomain-attribute/", base_url="http://sub1.test.test")
    eq_(b"Index", resp.data)

def test_bp_route_subdomain():
    resp = client.get("/subdomain-route/", base_url="http://sub2.test.test")
    eq_(b"Index", resp.data)

def test_bp_register_subdomain():
    resp = client.get("/basic/", base_url="http://sub3.test.test")
    eq_(b"Index", resp.data)

def test_bp_bp_subdomain():
    resp = client.get("/basic/", base_url="http://sub4.test.test")
    eq_(b"Index", resp.data)



