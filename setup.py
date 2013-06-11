"""
Flask-Classy
-------------

Class based views for Flask
"""
from setuptools import setup

setup(
    name='Flask-Classy',
    version='0.6.1',
    url='https://github.com/apiguy/flask-classy',
    license='BSD',
    author='Freedom Dumlao',
    author_email='freedomdumlao@gmail.com',
    description='Class based views for Flask',
    long_description=__doc__,
    py_modules=['flask_classy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_classy'
)