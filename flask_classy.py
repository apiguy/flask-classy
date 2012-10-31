"""
    Flask-Classy
    ------------

    Class based views for the Flask microframework.

    :copyright: (c) 2012 by Freedom Dumlao.
    :license: BSD, see LICENSE for more details.
"""

import inspect

def route(rule, **options):
    """A decorator that is used to define custom routes for methods in
    FlaskView subclasses. The format is exactly the same as Flask's
    `@app.route` decorator.
    """
    def decorator(f):
        if not hasattr(f, "routes"):
            f.routes = [(rule, options)]
        else:
            f.routes.append((rule, options))
        return f

    return decorator

class FlaskView(object):
    """Base view for any class based views implemented with Flask-Classy. Will
    automatically configure routes when registered with a Flask app instance.
    """

    @classmethod
    def register(cls, app, route_base=None):
        """Registers a FlaskView class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param route_base: the base path to use for all routes registered for
                           this class
        """

        if cls is FlaskView:
            raise TypeError("cls must be a subclass of FlaskVew, not FlaskView itself")

        if route_base:
            cls.route_base = route_base

        members = cls.find_member_methods()
        special_methods = ["get", "put", "post", "delete", "index"]
        id_methods = ["get", "put", "delete"]

        for name, value in members:
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)

            if hasattr(value, "routes"):
                for idx, rt in enumerate(value.routes):
                    rule, options = rt
                    rule = cls.build_rule(rule)
                    app.add_url_rule(rule, route_name + str(idx), proxy, **options)

            elif name in special_methods:
                methods = None
                if name in ["get", "index"]:
                    methods = ["GET"]
                elif name == "put":
                    methods = ["PUT"]
                elif name == "post":
                    methods = ["POST"]
                elif name == "delete":
                    methods = ["DELETE"]

                if name in id_methods:
                    rule = "/<id>/"
                else:
                    rule = "/"
                rule = cls.build_rule(rule)
                app.add_url_rule(rule, route_name, proxy, methods=methods)

            else:
                rule = cls.build_rule('/%s/' % name, value)
                app.add_url_rule(rule, route_name, proxy)

    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        def proxy(*args, **kwargs):
            i = cls()
            m = getattr(i, name)
            return m(*args, **kwargs)
        return proxy

    @classmethod
    def find_member_methods(cls):
        """Returns a list of methods that can be routed to"""

        base_members = dir(FlaskView)
        all_members = inspect.getmembers(cls, predicate=inspect.ismethod)
        return [member for member in all_members
                if not member[0] in base_members
                and not member[0].startswith("_")]

    @classmethod
    def build_rule(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `route_base` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """

        rule_parts = []
        route_base = cls.get_route_base()
        if route_base:
            rule_parts.append(route_base)

        rule = rule.strip("/")
        if rule:
            rule_parts.append(rule)

        if method:
            args = inspect.getargspec(method)[0]
            for arg in args:
                if arg != "self":
                    rule_parts.append("<%s>" % arg)

        return "/%s/" % "/".join(rule_parts)

    @classmethod
    def get_route_base(cls):
        """Returns the route base to use for the current class."""

        if hasattr(cls, "route_base"):
            route_base = cls.route_base
        else:
            if cls.__name__.endswith("View"):
                route_base = cls.__name__[:-4].lower()
            else:
                route_base = cls.__name__.lower()

        return route_base.strip("/")


    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ":%s" % method_name



