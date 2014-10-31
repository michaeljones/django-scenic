
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

