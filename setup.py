"""
Flask-Classy
-------------

Class based views for Flask
"""
from setuptools import setup

setup(
    name='Flask-Classy',
    version='0.6.8',
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
        'Flask>=0.9'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_classy'
)