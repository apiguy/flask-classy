from flask_classy import FlaskView, route

class BasicView(FlaskView):

    def index(self):
        """A docstring for testing that docstrings are set"""
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id

    def put(self, id):
        return "Put " + id

    def patch(self, id):
        return "Patch " + id

    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    def custom_method(self):
        return "Custom Method"

    def custom_method_with_params(self, p_one, p_two):
        return "Custom Method %s %s" % (p_one, p_two,)

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @route("/route1/")
    @route("/route2/")
    def multi_routed_method(self):
        return "Multi Routed Method"

    @route("/noslash")
    def no_slash_method(self):
        return "No Slash Method"

    @route("/endpoint/", endpoint="basic_endpoint")
    def custom_endpoint(self):
        return "Custom Endpoint"

    @route("/route3/", methods=['POST'])
    def custom_http_method(self):
        return "Custom HTTP Method"

class SubdomainAttributeView(FlaskView):
    subdomain = "sub1"

    def index(self):
        return "Index"

class SubdomainRouteView(FlaskView):

    @route("/", subdomain="sub2")
    def index(self):
        return "Index"

class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        return "Index"

class RouteBaseView(FlaskView):
    route_base = "/base-routed/"

    def index(self):
        return "Index"

class VarBaseView(FlaskView):
    route_base = "/var-base-route/<route>"

    def before_index(self):
        from flask import request
        request.view_args.pop('route')

    def index(self):
        return "Custom routed."

    def with_base_arg(self, route):
        return "Base route arg: " + route

class BeforeRequestView(FlaskView):

    def before_request(self, name):
        self.response = "Before Request"

    def index(self):
        return self.response

class BeforeViewView(FlaskView):

    def before_index(self):
        self.response = "Before View"

    def index(self):
        return self.response

class AfterViewView(FlaskView):

    def after_index(self, response):
        return "After View"

    def index(self):
        return "Index"

class AfterRequestView(FlaskView):

    def after_request(self, name, response):
        return "After Request"

    def index(self):
        return "Index"

class VariedMethodsView(FlaskView):

    def index(self):
        return "Index"

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @classmethod
    def class_method(cls):
        return "Class Method"


