
django-scenic: Composition Based Views
======================================

An approach to Django views favouring composition over inheritance.

Composition provides increased flexibility and better separation of concerns
when compared to inheritance and mixins. By changing our approach to building
views we can take advantage of using composition in our view creation.


Status
------

Available for the curious but still in early stages and likely to change.


Concepts
--------

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
~~~~~

Unfortunately, views use forms and conventional Django forms have to be
instantiated once per request and so Scenic provides support for building these
forms per-request but it would be interesting to explore a form framework that
was request independent to allow for potentially better integration into Scenic.


Design
------

Scenic relies on the composition of lots of small focussed immutable instances
of classes. Classes are used because composition is easiest with objects in
Python. If the currying of functions had a cleaner syntax in Python it might be
preferable to use them in places.


Comparisons
-----------

Function Based Views
~~~~~~~~~~~~~~~~~~~~

A simple template view ends up looking likely a unnecessarily complex version of
a Django function view for the same purpose which isn't a great start. The
Django function view code might look like::

   def object_detail(request, *args **kwargs):
       object = get_object_or_404(MyModel, pk=kwargs['pk'])

       return render(
           request,
           'mymodels/mymodel_list.html',
           {'object': object}
           )

The Scenic code looks like::

   def create_object_detail():
       queryset = MyModel.objects.all()
       object = SingleObject('pk', 'object', queryset)

       return template_view(
           'mymodels/mymodel_detail.html',
           sc.DictContext({'object': object})
           )

The difference comes when want to extend this. For example, adding a requirement
to be logged in we get::

   # --- Function based views
   @login_required
   def object_detail(request, *args **kwargs):
       object = get_object_or_404(MyModel.objects, pk=kwargs['pk'])

       return render_to_response(
           'mymodels/mymodel_list.html',
           {'object': object}
           )

   # --- Scenic based views
   def create_object_detail():
       queryset = MyModel.objects.all()
       object = SingleObject('pk', 'object', queryset)

       return LoginRequired(
          template_view(
              'mymodels/mymodel_detail.html',
              sc.DictContext({'object': object})
              )
          )

As the function based view is a directly called as a function, we need to use
Python decorators to wrap the 'login required' check around it. It is cleaner
with Scenic where you can simply wrap the returned view.

This basic example hits upon the core issue here. Flexibility comes from
composing elements of your program. Composition is only easy in Python with
objects and so you want to be in control of building the objects in your
program. Conventional function based views do not give you that control as the
function you specify in your view file is called directly to process the
request. It doesn't give you room to build an object stack, it just expects you
to start handling the request straight away.

So in the conventional function based view, instead of simple object composition
you need to start using decorators to fit inbetween your view and the framework.
It is a minor difference, but an important one. Django only ever wants a
callable object to give to the url routing code to handle the request. It is up
to us whether we take the time to construct that callable or hand Django a
simple function.

