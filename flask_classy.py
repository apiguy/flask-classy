"""
    Flask-Classy
    ------------

    Class based views for the Flask microframework.

    :copyright: (c) 2012 by Freedom Dumlao.
    :license: BSD, see LICENSE for more details.
"""

__version__ = "0.5.2"

import functools
import inspect
from werkzeug.routing import parse_rule
from flask import request, Response, make_response
import re

_temp_rule_cache = None

def route(rule, **options):
    """A decorator that is used to define custom routes for methods in
    FlaskView subclasses. The format is exactly the same as Flask's
    `@app.route` decorator.
    """

    def decorator(f):
        global _temp_rule_cache
        if _temp_rule_cache is None:
            _temp_rule_cache = {f.__name__: [(rule, options)]}
        elif not f.__name__ in _temp_rule_cache:
            _temp_rule_cache[f.__name__] = [(rule, options)]
        else:
            _temp_rule_cache[f.__name__].append((rule, options))

        return f

    return decorator

class _FlaskViewMeta(type):

    def __init__(cls, name, bases, dct):
        global _temp_rule_cache
        if _temp_rule_cache:
            cls._rule_cache = _temp_rule_cache
            _temp_rule_cache = None

class FlaskView(object):
    """Base view for any class based views implemented with Flask-Classy. Will
    automatically configure routes when registered with a Flask app instance.
    """

    __metaclass__ = _FlaskViewMeta

    #: A list of decorators to be applied to all view of this class
    decorators = []

    @classmethod
    def register(cls, app, route_base=None, subdomain=None):
        """Registers a FlaskView class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param route_base: The base path to use for all routes registered for
                           this class. Overrides the route_base attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.
        """

        if cls is FlaskView:
            raise TypeError("cls must be a subclass of FlaskVew, not FlaskView itself")

        if route_base:
            if hasattr(cls, "route_base"):
                cls.orig_route_base = cls.route_base

            cls.route_base = route_base

        if not subdomain:
            if hasattr(app, "subdomain") and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, "subdomain"):
                subdomain = cls.subdomain

        members = cls.find_member_methods()
        special_methods = ["get", "put", "patch", "post", "delete", "index"]

        for name, value in members:
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(cls, "_rule_cache") and name in cls._rule_cache:
                    for idx, cached_rule in enumerate(cls._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(cls._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "%s_%d" % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy, subdomain=subdomain, **options)

                elif name in special_methods:
                    if name in ["get", "index"]:
                        methods = ["GET"]
                    else:
                        methods = [name.upper()]

                    rule = cls.build_rule("/", value)

                    app.add_url_rule(rule, route_name, proxy, methods=methods, subdomain=subdomain)

                else:
                    rule = cls.build_rule('/%s/' % name, value,)
                    app.add_url_rule(rule, route_name, proxy, subdomain=subdomain)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError("Incompatible decorator detected on %s in class %s" % (name, cls.__name__))

        if hasattr(cls, "orig_route_base"):
            cls.route_base = cls.orig_route_base
            del cls.orig_route_base



    @classmethod
    def parse_options(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return subdomain, endpoint, options,


    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                i.before_request(name, **request.view_args)

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                before_view(**request.view_args)

            response = view(**request.view_args)
            if not isinstance(response, Response):
                response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def find_member_methods(cls):
        """Returns a list of methods that can be routed to"""

        base_members = dir(FlaskView)
        all_members = inspect.getmembers(cls, predicate=inspect.ismethod)
        return [member for member in all_members
                if not member[0] in base_members
                and not member[1].im_self == cls
                and not member[0].startswith("_")
                and not member[0].startswith("before_")
                and not member[0].startswith("after_")]

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

        route_base = cls.get_route_base()
        rule_parts = [route_base, rule]
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method:
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append("<%s>" % arg)

        result = "/%s" % "/".join(rule_parts)
        return re.sub(r'(/)\1+', r'\1', result)

    @classmethod
    def get_route_base(cls):
        """Returns the route base to use for the current class."""

        if hasattr(cls, "route_base"):
            route_base = cls.route_base
            base_rule = parse_rule(route_base)
            cls.base_args = [r[2] for r in base_rule]
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


def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, 'func_closure') or method.func_closure is None:
        raise DecoratorCompatibilityError

    method = method.func_closure[0].cell_contents
    return get_true_argspec(method)


class DecoratorCompatibilityError(Exception):
    pass






