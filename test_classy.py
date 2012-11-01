import unittest
from flask import Flask
from flask_classy import FlaskView, route

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

    def params_view(self, arg1, arg2):
        return "Params View %s %s" % (arg1, arg2,)

class IndexTestView(FlaskView):
    route_base = "/"

    def index(self):
        return "Home Page"

class CommonTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        BasicTestView.register(self.app)
        IndexTestView.register(self.app)

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

    def test_params_view(self):
        res = self.client.get("/basictest/params_view/1234/5678/")
        self.assertEqual("Params View 1234 5678", res.data)

    def test_index_route_base(self):
        res = self.client.get("/")
        self.assertEqual("Home Page", res.data)

    def tearDown(self):
        pass

if __name__ == "main":
    unittest.main()