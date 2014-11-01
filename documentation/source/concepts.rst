
Concepts
========

Django's class-based-views provide a framework to create view classes which are
automatically instantiated once per-request. As Django is responsible for
instantiating the view classes, their construction has to be quite simple and
flexibility can only be introduced through class attributes and inheritance.

This can provide quite concise code for simple cases but further extensions tend
towards an ugly mix of concerns as inheritance is a poor method for composing
functionality.

The Scenic approach is to create view classes which are only instantiated once,
by the client code, and are used across requests. Then as the client code is
responsibly for the instantiation of the view classes there is much greater
potential for composing a network of small objects together with clean
separation of concerns and easy points for extension.

This approach does mean that you cannot store request state on the view
instances but this is avoided by including a ``state`` object which is passed
through for each request.


Forms
-----

Unfortunately, views use forms and conventional Django forms have to be
instantiated once per request and so Scenic provides support for building these
forms per-request but it would be interesting to explore a form framework that
was request independent to allow for potentially better integration into Scenic.


