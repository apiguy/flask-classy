Flask-Classy
=============

.. module:: flask.ext.classy

Flask-Classy is an extension that adds class-based views to Flask.
But why?

I ❤ Flask. Like a lot. But I sometimes projects get a little big
and need some way of managing and organizing all the different
pieces. I know what you're saying: "But what about Blueprints?"

You're right. Blueprints are pretty awesome. But I found that they
aren't always enough to encapsulate a specific context the way I
need. What I wanted, no what I *needed* was to be able to group
my views into relevant classes each with their own context and
behavior. It's also made testing really nifty too.

"But Mr. ApiGuy, my projects aren't that big. Can Flask-Classy do
anything else for me besides making a big project easier to manage?"

Why yes. It does help a bit with one other thing.

Flask-Classy makes dealing with multiple HTTP methods for a single
url or resource much easier by being _smart_ about certain method
names in your views. For example, if you have a method named `get`
Flask-Classy will *get* what you are trying to do and generate
a route automatically that accepts *GET* requests!

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
that a random quote is returned each time. Voila!

So by now you must be keenly aware of the fact that you have not defined a
single route, but yet routing is obviously taking place. "Is this voodoo?"
you ask?

Not at all. Flask-Classy will automatically create routes for any method
in a FlaskView that doesn't begin with an underscore character.
You can still define your own routes of course, and we'll look at that next.

Using custom routes
~~~~~~~~~~~~~~~~~~~

So let's pretend that `/quotes/random/` is just too unsightly and we must
fix it to be something more spectacular forthwith. In a moment of blind
inspiration we decide that getting a random quote is on par with receiving
a rasher of your favorite porcine delicacy. The new url should be `/quotes/word_bacon/`
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

Load up http://localhost/quotes/word_bacon/ in your browser and behold
your latest achievement.

The route decorator takes exactly the same parameters as Flask's `app.route`
decorator, so you should feel right at home adding custom routes to any
views you create.

So far, all of our urls have been prefixed by that `/quotes` bit and you
have probably deduced that it was derived from the name of your FlaskView
instance (minus the "View" suffix, of course.) "That's all well and good,"
you're saying, "but how do I change that? What if I want my views at the
root?" Well, person, I have an answer for you.

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

Special method names
~~~~~~~~~~~~~~~~~~~~

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
    and lists of resources. The automatically generated route is::

        rule:   '/'
        name:   <class name>:index
        method: GET

**get**
    Another old familiar friend, `get` is usually used to retrieve a
    specific resource. The automatically generated route is::

        rule:   '/<id>/'
        name:   <class name>:get
        method: GET

**post**
    This method is generally used for creating new instances of a resource
    but can really be used to handle any posted data you want. The
    automatically generated route is::

        rule:   '/'
        name:   <class name>:post
        method: POST

**put**
    For those of us using REST this one is really helpful. It's generally
    used to update a specific resource. The automatically generated route
    is::

        rule:   '/<id>/'
        name:   <class name>:put
        method: PUT

**delete**
    More RESTfulness. It's the most self explanitory of all the RESTful
    methods, and it's commonly used to destroy a specific resource. The
    automatically generated route is::

        rule:   '/<id>/'
        name:   <class name>:delete
        method: DELETE


Your own methods (they're special too!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

And lastly, but not leastly, let's talk about how you can add your
own methods (like we did with `random` back in the day, remember?
Good times.) If you add your own methods `FlaskView` will detect them
during registration and register routes for them, whether you've
gone and defined your own, or you just want to let `FlaskView` do it's
thing. By default, `FlaskView` will create a route that is the same as
the method name. It doesn't look for parameters though, so if your
method takes them and you haven't defined a route, you're gonna have a
bad time. That'll be coming soon though, so don't you worry.

Questions?
----------

Feel free to ping me on twitter @apiguy, or head on over to the
github repo at http://github.com/apiguy/flask-classy so you can join
the fun.