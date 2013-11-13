Flask-Classy
=============

.. module:: flask.ext.classy

Flask-Classy is an extension that adds class-based views to Flask.
But why?

I ❤ Flask. Like a lot. But sometimes projects get a little big
and I need some way of managing and organizing all the different
pieces. I know what you're saying: "But what about Blueprints?"

You're right. Blueprints are pretty awesome. But I found that they
aren't always enough to encapsulate a specific context the way I
need. What I wanted, no what I *needed* was to be able to group
my views into relevant classes each with their own context and
behavior. It's also made testing really nifty too.

"OK, I see your point. But can't I just use the base classes in
``flask.views`` to do that?"

Well, yes and no. While ``flask.views.MethodView`` does
provide some of the functionality of ``flask.ext.classy.FlaskView``
it doesn't quite complete the picture by supporting methods that
aren't part of the typical CRUD operations for a given resource, or
make it easy for me to override the route rules for particular view.
And while ``flask.views.View`` does add some context, it requires
a class for each view instead of letting me group very similar
views for the same resource into a single class.

"But my projects aren't that big. Can Flask-Classy do
anything else for me besides making a big project easier to manage?"

Why yes. It does help a bit with some other things.

For example, `Flask-Classy` will automatically generate routes based on the methods
in your views, and makes it super simple to override those routes
using Flask's familiar decorator syntax.

.. _Flask-Classy: http://github.com/apiguy/flask-classy
.. _Flask: http://flask.pocoo.org/

Installation
------------

Install the extension with::

    $ pip install flask-classy

or if you're kickin' it old-school::
    
    $ easy_install flask-classy

Let's see how it works
----------------------

If you're like me, you probably get a better idea of how to use something
when you see it being used. Let's go ahead and create a little app to
see how Flask-Classy works::

    from flask import Flask
    from flask.ext.classy import FlaskView

    # we'll make a list to hold some quotes for our app
    quotes = [
        "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
        "If there is a way to do it better... find it. ~ Thomas Edison",
        "No one knows what he can do till he tries. ~ Publilius Syrus"
    ]

    app = Flask(__name__)

    class QuotesView(FlaskView):
        def index(self):
            return "<br>".join(quotes)

    QuotesView.register(app)

    if __name__ == '__main__':
        app.run()

Run this app and open your web browser to: http://localhost:5000/quotes/

As you can see, it returns the list of quotes. But what if we just wanted
one quote? What would we do then?

::

    class QuotesView(FlaskView):
        def index(self):
            ...

        def get(self, id):
            id = int(id)
            if id < len(quotes) - 1:
                return quotes[id]
            else:
                return "Not Found", 404

Now direct your browser to: http://localhost:5000/quotes/1/ and you should
see the very poignant quote from the esteemed Mr. Edison.

That's cool and all, but what if we just wanted a random quote? What then?
Let's add a random view to our FlaskView::

    from random import choice

::

    class QuotesView(FlaskView):
        def index(self):
            ...

        def get(self, id):
            ...

        def random(self):
            return choice(quotes)

And point your browser to: http://localhost:5000/quotes/random/ and see
that a random quote is returned each time. Voilà!

So by now you must be keenly aware of the fact that you have not defined a
single route, but yet routing is obviously taking place. "Is this voodoo?"
you ask?

Not at all. Flask-Classy will automatically create routes for any method
in a FlaskView that doesn't begin with an underscore character.
You can still define your own routes of course, and we'll look at that next.



Using custom routes
-------------------

So let's pretend that `/quotes/random/` is just too unsightly and we must
fix it to be something more spectacular forthwith. In a moment of blind
inspiration we decide that getting a random quote is on par with receiving
a rasher of your favorite porcine delicacy. The new URL should be `/quotes/word_bacon/`
so that everyone knows what a treat they are in for.

::

    from flask.ext.classy import FlaskView, route

::

    class QuotesView(FlaskView):
        def index(self):
            ...

        def get(self, id):
            ...

        @route('/word_bacon/') #<--- Adding route
        def random(self):
            return choice(quotes)

Load up http://localhost:5000/quotes/word_bacon/ in your browser and behold
your latest achievement.

The route decorator takes exactly the same parameters as Flask's `app.route`
decorator, so you should feel right at home adding custom routes to any
views you create.

.. note::
    If you want to use other decorators with your views, you'll need to
    make sure that the ``@route`` decorators are first.

So far, all of our URLs have been prefixed by that `/quotes` bit and you
have probably deduced that it was derived from the name of your FlaskView
instance (minus the "View" suffix, of course.) "That's all well and good,"
you're saying, "but how do I change that? What if I want my views at the
root?" Well, person, I have an answer for you.


Flask-Classy's way of talking about "routes"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OK, So I don't want to start inventing a new language (actually I'd love to
invent a new language, just not right now...) for talking about URLs, but
since Flask-Classy gives you a lot of flexibility in customizing your routes
we might as well make sure we're talking about the same things when we talk
about what you can do.

What you see below is a route comprised of a route prefix, and a route base:

    /neat_prefix/great_base/

The prefix `/neat_prefix/` is only included if you explicitly specify 
a prefix for the FlaskView, otherwise no prefix will be applied.

The route base `/great_base/` will always exist, either because it was
inferred automatically from the name of the FlaskView class, or because you
specified a route base to use.

.. note::
    Flask-Classy favors putting trailing slashes at the end of routes without parameters.
    You can override this behavior by specifying `trailing_slash=False` either
    as an attribute of your `FlaskView` or in the `register` method.


Specifying a Route Prefix
~~~~~~~~~~~~~~~~~~~~~~~~~

A route prefix is a great way to define a common base to URLs. For example lets
say you had a bunch of views that were all part of your application's API system.

You *could* write custom route bases for all of them, but if you want to use
Flask Classy's (admittedly amazing) automatic route generation stuff you'll lose
the part where it infers the route base from the name of the class.

A better choice is to use a route prefix.

You can specify a route prefix either as an attribute of the FlaskView, or when you
register the FlaskView with the application.

As an attribute:
****************

Using an attribute is a great way to define a default prefix, as you can always
override this value when you register the FlaskView with your app::

    class BurgundyView(FlaskView):
        route_prefix = '/colors/'

        def index(self):
            ...

When registering:
*****************

Alternatively (or additionally, if you like) you can specify a route prefix when
you register the route with your app::

    BurgundyView.register(app, route_prefix='/redish_colors/')

And this will override any route prefixes set on the FlaskView class itself.



Customizing the Route Base
~~~~~~~~~~~~~~~~~~~~~~~~~~

There are 2 ways to customize the base route of a `FlaskView`. (Well
technically there are 3 if you count changing the name of the class
but that's hardly a reasonable way to go about it.)

Method 1:
*********

The first method simply requires you to set a `route_base` attribute on
your `FlaskView`. Suppose we wanted to make our QuotesView handle the
root of the web application::

    class QuotesView(FlaskView):
        route_base = '/'

        def index(self):
            ...

        def get(self, id):
            ...

        @route('/word_bacon/')
        def random(self):
            ...

Method 2:
*********

The second method is perfect for when you're using app factories, and
you need to be able to specify different base routes for different apps.
You can specify the route when you register the class with the Flask app
instance::

    QuotesView.register(app, route_base='/')

The second method will always override the first, so you can use method
one, and override it with method two if needed. Sweet!

Using multiple routes for a single view
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What happens when you need to apply more than one route to a specific view
(for what it's worth, Flask core developer Armin Ronacher `says doing that is
a bad idea <http://stackoverflow.com/a/7876088/105987>`_). But since you're so
determined let's see how to do that anyway.

So let's say you add the following routes to one of your views::

    class QuotesView(FlaskView):
        route_base = '/'

        @route('/quote/<id>')
        @route('/quote/show/<id>')
        def show_quote(self, id):
            ...

That would end up generating the following 2 routes:

============ ================================
**rule**     /quote/<id>
**endpoint** QuotesView:show_quote_1
**method**   GET
============ ================================

============ ================================
**rule**     /quote/show/<id>
**endpoint** QuotesView:show_quote_0
**method**   GET
============ ================================

"Oh weird! What's with all the _0 and _1 stuff?" you ask in disgust. Well
first I want to know how you managed to pronounce _0. But really the reason
is that since there is more than one route, an index is added to prevent an
endpoint collision. This differs from the default behavior of `Flask`, which
allows you to create collisions.


Specify your own damn endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So you don't like the nifty indexing trick? Well fine then. I guess you can
go ahead and specify your own endpoint if you like but that's only because I
like you.

::

    class QuotesView(FlaskView):
        route_base = '/'

        @route('/quote/<id>', endpoint='show_quote')
        @route('/quote/show/<id>')
        def show_quote(self, id):
            ...

Will generate the following routes:

============ ================================
**rule**     /quote/<id>
**endpoint** show_quote
**method**   GET
============ ================================

============ ================================
**rule**     /quote/show/<id>
**endpoint** QuotesView:show_quote_0
**method**   GET
============ ================================

Special method names
--------------------

So I guess I have to break the narrative a bit here so I can take some
time to talk about `Flask-Classy`'s special method names.

Here's the thing. `FlaskView` is smart. No, not solving differential
equations smart, but let's just say it knows how to put the round peg
in the round hole. When you register a `FlaskView` with an app,
`FlaskView` will look for special methods in your class. Why? Because
I care. I know that sometimes you just want things to just *work* and
not have to think about it. Let's look at `FlaskView`'s very special
method names:

**index**
    Woah... you've seen this one before! Remember way back at the
    beginning? Oh nevermind. So *index* is generally used for home pages
    and lists of resources. The automatically generated route is:

    ============ ================================
    **rule**     /
    **endpoint** <class name>:index
    **method**   GET
    ============ ================================

**get**
    Another old familiar friend, `get` is usually used to retrieve a
    specific resource. The automatically generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:get
    **method**   GET
    ============ ================================

**post**
    This method is generally used for creating new instances of a resource
    but can really be used to handle any posted data you want. The
    automatically generated route is:

    ============ ================================
    **rule**     /
    **endpoint** <class name>:post
    **method**   POST
    ============ ================================

**put**
    For those of us using REST this one is really helpful. It's generally
    used to update a specific resource. The automatically generated route
    is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:put
    **method**   PUT
    ============ ================================

**patch**
    Similar to `put`, `patch` is used for updating a resource. Unlike `put`
    however you only send the parts of the resource you want changed,
    instead of doing a complete replacement of the resource. The automatically
    generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:patch
    **method**   PATCH
    ============ ================================

**delete**
    More RESTfulness. It's the most self explanatory of all the RESTful
    methods, and it's commonly used to destroy a specific resource. The
    automatically generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:delete
    **method**   DELETE
    ============ ================================


url_for art thou, Romeo?
--------------------------

Sorry that's a terrible name for a section header, but naming things is what
am the least skilled at, so please bear with me.

Once you've got your `FlaskView` registered, you'll probably want to be able
to get the URLs for it in your templates and redirects and whatnot. Flask
ships with the awesome `url_for` function that does an excellent job of
turning a function name into a URL that maps to it. You can use `url_for`
with Flask-Classy by using the format "<Class name>:<method name>". Let's
look at an example::

    class DuckyView(FlaskView):
        def index(self):
            return "Duckies!"

        def get(self, name):
            return "Duck %s" % name

        @route('/do_duck_stuff', endpoint='do_duck_stuff')
        def post(self):
            return "Um... Quack?"

In this example, you can get a URL to the index method using::

    url_for("DuckyView:index")

And you can get a URL to the get method using::

    url_for("DuckyView:get", name="Howard")

And for that view with the custom endpoint defined?::

    url_for("do_duck_stuff")

.. note::
    Notice that the custom endpoint does not get prefixed with the class
    name like the auto-generated endpoints. When you define a custom
    endpoint, we hand that over to Flask in it's original, unaltered form.


Your own methods (they're special too!)
---------------------------------------

Let's talk about how you can add your own methods (like we did with
`random` back in the day, remember? Good times.) If you add your own
methods `FlaskView` will detect them during registration and register
routes for them, whether you've gone and defined your own, or you just
want to let `FlaskView` do it's thing. By default, `FlaskView` will
create a route that is the same as the method name. So if you define a
view method in your `FlaskView` like this::

    class SomeView(FlaskView):
        route_base = "root"

        def my_view(self):
            return "Check out my view!"

`FlaskView` will generate a route like this:

============ ================================
**rule**      /some/my_view/
**endpoint**  SomeView:my_view
**method**    GET
============ ================================

"That's fine." you say. "But what if I have a view method with some
parameters?" Well `FlaskView` will try to take care of that for you
too. If you were to define another view like this::

    class AnotherView(FlaskView):
        route_base = "home"

        def this_view(self, arg1, arg2):
            return "Args: %s, %s" % (arg1, arg2,)

`FlaskView` would generate a route like this:

============ ================================
**rule**     /home/this_view/<arg1>/<arg2>
**endpoint** AnotherView:this_view
**method**   GET
============ ================================

.. note::
    One important thing to note, is that `FlaskView` does not type your
    parameters, so if you want or need them you'll need to define the
    route yourself using the `@route` decorator.


Decorating Tips
---------------

So if you're like me (and who isn't?), you think that FlaskViews are
frickin' beautiful. But once you've moved in it's nice to add a little
personal touch, don't you think?

Of course I'm talking about decorators. The `Flask` ecosystem is full of
excellent extensions that allow you to customize a view's behavior
simply by adding a decorator, and you can use them with your
FlaskView's too.::

    class BetterButterView(FlaskView):

        @login_required  # Ain't it pretty?
        def super_secret(self):
            return "It's a secret to everyone."

But what about when you want to add a decorator to every method in your
`FlaskView`? All you need to do is add a `decorators` attribute to the
class definition with a list of decorators you want applied to every
method and `Flask-Classy` will take care of the rest::

    class WhataGreatView(FlaskView):
        decorators = [login_required]

        def this_is_secret(self):
            return "If you see this, you're logged in."

        def so_is_this(self):
            return "Looking at me? I guess you're logged in."


Before and After
----------------

Hey, remember that time when you made that big ol' `Flask` app and then
had those ``@app.before_reqeust`` and ``@app.after_request``
decorated methods? Remember how you only wanted some of them to run for
certain views so you had all those ``if view == the_one_I_care_about:``
statements and stuff?

**Yuck.**

I've been there too, and I think you might like how `Flask-Classy`
addresses this very touchy issue. ``FlaskView`` will look for wrapper
methods when your request is being processed so that you can create more
fine grained "before and after" processing methods.

Wrap all the views in a FlaskView
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So there you are, eating a delicious Strawberry Frosted Pop Tart one
morning, thinking about the awesome `Flask-Classy` app you deployed the
night before during one of your late night hackathons and it hits you:

*"Tracking! I need to track those widgets!"*

No doubt it's an inspired thought, but in this case it was a tragic
oversight. You realize now how lucky it was that you chose to use
`Flask-Classy` because adding tracking is going to be a snap::

    from flask.ext.classy import FlaskView
    from made_up_tracking import track_it

    class WidgetsView(FlaskView):

        def before_request(self, name):
            track_it("something is happening to a widget")

        def after_request(self, name, response):
            track_it("something happened to a widget")
            return response

        def post(self):
            ...

        def get(self, id):
            ...

Whew. Crisis averted, am I right? So you go about your day and at lunch time
you hit your favorite Bacon Sandwich place and start daydreaming about your
life as a rockstar `Flask-Classy` consultant when suddenly:

*"I really only care about when widgets are created and retrieved!"*

Wrap only specific views
~~~~~~~~~~~~~~~~~~~~~~~~

Yep, you've got a granularity problem. Not to worry though because
`Flask-Classy` is happy to let you know that it has *smart* wrapper methods
too. Let's say for example you wanted to run something before the ``index`` view
runs? Just create a method called ``before_index`` and `Flask-Classy` will make
sure it gets run only before that view. (as you have guessed by now,
``after_index`` will be run only after the index view).

::

    from flask.ext.classy import FlaskView
    from made_up_tracking import track_it

    class WidgetsView(FlaskView):

        # Will be run before the 'get' view
        def before_get(self):
            track_it("a widget is being accessed")

        # Will be run before the 'post' view
        def after_post(self, response):
            track_it("a widget was created")
            return response

        def post(self):
            ...

        def get(self, id):
            ...

The View Wrappin' Method List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just to be certain, let's go ahead and review the methods you can write to
wrap your views:

**before_request(self, name, *args, *kwargs)**
    Will be called before any view in this ``FlaskView`` is called.

    :name:       The name of the view that's about to be called.


    :\*args:     Any arguments that will be passed to the view.


    :\*\*kwargs: Any keyword arguments that will be passed to the view.


**before_<view_method>(self, *args, **kwargs)**
    Will be called before the view specified <view_method> is called.

    :\*args:     Any arguments that will be passed to the view.


    :\*\*kwargs: Any keyword arguments that will be passed to the view.


**after_request(self, name, response)**
    Will be called after any view in this ``FlaskView`` is called. You must
    return either the passed in response or a new response.

    :name:       The name of the view that was called.


    :response:   The response produced after calling the view.


**after_<view_method>(self, response)**
    Will be called after the <view_method> is called. You must return either
    the passed in response or a new response.

    :response:   The response produced after calling the view.


Order of Wrapped Method Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wrapper methods are called in the same order every time. "How predictable."
you're thinking. (You're starting to sound like my ex, sheesh.) I prefer the
term *reliable*.

1. Any method registered with ``@app.before_request``
2. FlaskView's ``before_request`` method
3. FlaskView's ``before_<view_method>`` method
4. The actual view method
5. FlaskView's ``after_<view_method>`` method
6. FlaskView's ``after_request`` method
7. Any method registered with ``@app.after_request``

Subdomains (getting advanced 'n stuff)
--------------------------------------

By now, you've built a few hundred `Flask` apps using `Flask-Classy`
and you probably think you're an expert. But not until you've tried
the snazzy `Subdomains` feature my friend.

Flask-Classy allows you to specify a subdomain to be used when
registering routes for your FlaskViews. While the usefulness of this
feature is probably apparent to many of you, let's go ahead and take a
look at one of the many facilitative use cases.

Suppose you've got a sweet API you're porting over from a legacy app
and in the migration you want to clean things up a bit and start using
a subdomain like ``api.socool.biz`` instead of the old way of accessing
it using ``api`` at the root of the path like ``socool.biz/api``. The
only catch, of course, is that you have API clients still using that
old path based method. What is a hard working developer like you to do?

Thanks to `Flask` and `Flask-Classy` you have some options. There are two
easy ways you can choose from to tell `Flask-Classy` which subdomains your
``FlaskView`` should respond to.

Let's see both methods so you can choose which one works best for your
application.

The Define-During-Registration Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Probably the most flexible method, you can define which subdomains you
want to support at the same time you're registering your views::

    # views.py

    from flask.ext.classy import FlaskView

    class CoolApiView(FlaskView):

        def index(self):
            return "API stuff"

::

    # main.py

    from flask import Flask
    from views import CoolApiView

    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'socool.biz'

    # This one matches URLs like: http://socool.biz/api/...
    CoolApiView.register(app, route_base='/api/')

    # This one matches URLs like: http://api.socool.biz/...
    CoolApiView.register(app, route_base='/', subdomain='api')

    if __name__ == "__main__":
        app.run()

The Explicit-Define-In-The-FlaskView Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using this method, you can explicitly define a subdomain as an attribute of
the ``FlaskView`` subclass::

    # views.py

    from flask.ext.classy import FlaskView

    class CoolApiView(FlaskView):
        subdomain = "api"

        def index(self):
            return "API Stuff"

::

    # main.py

    from flask import Flask
    from views import CoolApiView

    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'socool.biz'

    # This one matches URLs like: http://socool.biz/api/...
    CoolApiView.register(app, route_base='/api/', subdomain='')

    # This one matches URLs like: http://api.socool.biz/...
    CoolApiView.register(app, route_base="/")

    if __name__ == "__main__":
        app.run()

As you can see here, specifying the subdomain to the register method will
override the explicit subdomain attribute set inside the class.


Adding Resource Representations (Get real classy and put on a top hat)
----------------------------------------------------------------------
So, you want to use Flask-Classy to make a RESTful API. Not a problem, we got
you covered. Say you want your API to be able to respond to requests with JSON.
All you have to do is create a class that defines how to serialize and deserialize
the data, add it to the `representations` variable on your `FlaskView`.

Here's the code for the JSON Response class::

    # representations.py
    
    import json
    from flask import make_response

    class JsonResource(object):
        content_type = 'application/json'

        def output(self, data, code, headers=None):
            dumped = json.dumps(data)
            response = make_response(dumped, code)
            if headers:
                headers.extend({'Content-Type': self.content_type})
            else:
                headers = {'Content-Type': self.content_type}
            response.headers.extend(headers)

            return response


        def input(self, data):
            loaded = loads(data)
            
            return loaded

::

The go ahead and add this new resource representation to your `FlaskView`::

    # views.py

    from flask.ext.classy import FlaskView
    from representations import JsonResource

    class CoolJSONView(FlaskView):
        representations = {'application/json': JsonResource()}

        def index(self):
            return {'This is JSON': 'How Cool is that'}

::


Questions?
----------

Feel free to ping me on twitter @apiguy, or head on over to the
github repo at http://github.com/apiguy/flask-classy so you can join
the fun.


API
---
.. autoclass:: flask.ext.classy.FlaskView
    :members:


.. autofunction:: flask.ext.classy.route

----

© Copyright 2013 by Freedom Dumlao, `Follow Me @apiguy <https://twitter.com/APIguy>`_
