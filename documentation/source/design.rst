
Design
======

Scenic relies on the composition of lots of small focussed immutable instances
of classes. Classes are used because composition is easiest with objects in
Python. If the currying of functions had a cleaner syntax in Python it might be
preferable to use them in places.


Hierarchy
---------

Scenic follows the following composition hierarchy for views:

- Guards
  - View
    - MethodHandler
      - Response

Simple GET method handlers follow the pattern:

- MethodHandler
  - TemplateResponse
    - Template

Simple POST method handlers follow the pattern:

- MethodHandler
  - Form
  - Valid Response
  - Invalid Response

Which tends to look like:

- MethodHandler
  - Form
  - RedirectResponse
    - Url
    - Form Success Action
  - Template Response
    - Template
