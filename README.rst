
django-scenic: Composition Based Views
======================================

An approach to Django views favouring composition over inheritance.

Composition provides increased flexibility and better separation of concerns
when compared to inheritance and mixins. By changing our approach to building
views we can take advantage of using composition in our view creation.


Concepts
--------

Django's class-based-views provide a framework to create view classes which are
automatically instantiated once per-request. As Django is responsible for
instantiating the view classes, theirconstruction has to be quite simple and
flexibility has to be introduced through class attributes and inheritance.

This can provide quite concise code for simple cases but further extensions tend
towards an ugly mix of concerns as inheritance is a poor method for composing
functionality.

The Scenic approach is to create view classes which are only instantiated once,
by the client code, and are used across requests. This means that you cannot
store request state on the view classes any more but this is avoided by
including a ``state`` object which is passed through for each request. Then as
the client code is responsibly for the instantiation of the view classes there
is much greater potential for composing a network of small objects together
with clean separation of concerns and easy points for extension.
