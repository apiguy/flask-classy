import unittest
from flask import Flask
from flask_classy import FlaskView, route

def test_decorator(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

class BasicTestView(FlaskView):

    def index(self):
        return "Index"

    def get(self, id):
        return "Get " + id

    def put(self, id):
        return "Put " + id

    def patch(self, id):
        return "Patch " + id

    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    def other_method(self):
        return "Other Method"

    @route("/another")
    def another_method(self):
        return "Another Method"

    @route("/route1")
    @route("/route2")
    def multi_route(self):
        return "Multi Route"

    @test_decorator
    @route("/stacked")
    def stacked_decorators(self):
        return "Stacked"

    @test_decorator
    def other_decorator(self):
        return "Other Decorator"

    def params_view(self, arg1, arg2):
        return "Params View %s %s" % (arg1, arg2,)

class IndexTestView(FlaskView):
    route_base = "/"

    def index(self):
        return "Home Page"

class SubdomainTestView(FlaskView):
    route_base = "/sub"
    subdomain = "sub"

    def sub(self):
        return "Subdomain"

class CommonTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.app.config['SERVER_NAME'] = 'test.test'
        self.client = self.app.test_client()

        BasicTestView.register(self.app)
        IndexTestView.register(self.app)
        SubdomainTestView.register(self.app)
        SubdomainTestView.register(self.app, subdomain="sub2")

    def test_basic_index(self):
        res = self.client.get("/basictest/")
        self.assertEqual("Index", res.data)

    def test_basic_get(self):
        res = self.client.get("/basictest/1234/")
        self.assertEqual("Get 1234", res.data)

    def test_basic_put(self):
        res = self.client.put("/basictest/1234/")
        self.assertEqual("Put 1234", res.data)

    def test_basic_patch(self):
        res = self.client.patch("/basictest/1234/")
        self.assertEqual("Patch 1234", res.data)

    def test_basic_post(self):
        res = self.client.post("/basictest/")
        self.assertEqual("Post", res.data)

    def test_basic_delete(self):
        res = self.client.delete("/basictest/1234/")
        self.assertEqual("Delete 1234", res.data)

    def test_basic_method(self):
        res = self.client.get("/basictest/other_method/")
        self.assertEqual("Other Method", res.data)

    def test_routed_method(self):
        res = self.client.get("/basictest/another/")
        self.assertEqual("Another Method", res.data)

        #.Make sure the automatic route wasn't generated
        res = self.client.get("/basictest/another_method/")
        self.assertNotEqual("Another Method", res.data)

    def test_multiple_routed_method(self):
        res = self.client.get("/basictest/route1/")
        self.assertEqual("Multi Route", res.data)
        res = self.client.get("/basictest/route2/")
        self.assertEqual("Multi Route", res.data)

    def test_stacked_decorators(self):
        res = self.client.get("/basictest/stacked/")
        self.assertEqual("Stacked", res.data)

    def test_other_decorator(self):
        res = self.client.get("/basictest/other_decorator/")
        self.assertEqual("Other Decorator", res.data)

    def test_params_view(self):
        res = self.client.get("/basictest/params_view/1234/5678/")
        self.assertEqual("Params View 1234 5678", res.data)

    def test_index_route_base(self):
        res = self.client.get("/")
        self.assertEqual("Home Page", res.data)

    def test_subdomain(self):
        res = self.client.get("/sub/sub/")
        self.assertNotEqual("Subdomain", res.data)

        res = self.client.get("/sub/sub/", base_url='http://sub.test.test/')
        self.assertEqual("Subdomain", res.data)

        res = self.client.get("/sub/sub/", base_url='http://sub2.test.test/')
        self.assertEqual("Subdomain", res.data)

    def tearDown(self):
        pass

if __name__ == "main":
    unittest.main()