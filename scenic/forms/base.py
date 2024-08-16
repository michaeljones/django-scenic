
import copy

from django.core.exceptions import ValidationError
from django.forms.fields import FileField
from django.forms.utils import flatatt, ErrorDict, ErrorList, pretty_name
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.widgets import TextInput, Textarea
from django.utils.encoding import smart_str
from django.utils.html import conditional_escape, format_html
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


NON_FIELD_ERRORS = '__all__'


class FormState(object):

    def __init__(self, initial, data=None, files=None):
        self.data = data or {}
        self.files = files or {}
        self.errors = ErrorDict()
        self.initial = initial

    @property
    def is_bound(self):
        return bool(self.data or self.files)


def build_form_state(state, context, form):

    initial_data = {}
    for key, value in form.initial:
        initial_data[key] = value(state, context)

    return FormState(initial_data, context.request.POST, context.request.FILES)


class BaseForm(object):

    def __init__(self, initial=None, auto_id='id_%s', prefix=None, error_class=ErrorList):
        # self.is_bound = data is not None or files is not None
        # self.data = data or {}
        # self.files = files or {}
        self.auto_id = auto_id
        self.prefix = prefix
        self.initial = initial or {}
        self.error_class = error_class
        # # Translators: This is the default suffix added to form field labels
        # self.label_suffix = label_suffix if label_suffix is not None else _(':')
        # self.empty_permitted = empty_permitted
        # self._errors = None # Stores the errors after clean() has been called.
        # self._changed_data = None

        # The base_fields class attribute is the *class-wide* definition of
        # fields. Because a particular *instance* of the class might want to
        # alter self.fields, we create self.fields here by copying base_fields.
        # Instances should always modify self.fields; they should not modify
        # self.base_fields.
        self.fields = copy.deepcopy(self.base_fields)

    # def __getitem__(self, name):
    #     "Returns a BoundField with the given name."
    #     try:
    #         field = self.fields[name]
    #     except KeyError:
    #         raise KeyError('Key %r not found in Form' % name)
    #     return BoundField(self, field, name)

    def add_prefix(self, field_name):
        """
        Returns the field name with a prefix appended, if this Form has a
        prefix set.

        Subclasses may wish to override.
        """
        return '%s-%s' % (self.prefix, field_name) if self.prefix else field_name

    def add_initial_prefix(self, field_name):
        """
        Add a 'initial' prefix for checking dynamic initial values
        """
        return 'initial-%s' % self.add_prefix(field_name)

    def _clean_fields(self, form_state, cleaned_data, errors):

        data = form_state.data
        files = form_state.files

        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(data, files, name)
            try:
                if isinstance(field, FileField):
                    initial = form_state.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    method = getattr(self, 'clean_%s' % name)
                    value = method(form_state, cleaned_data)
                    cleaned_data[name] = value
            except ValidationError as e:
                errors[name] = self.error_class(e.messages)
                if name in cleaned_data:
                    del cleaned_data[name]

    def _validate(self, form_state, cleaned_data, errors):

        self._clean_fields(form_state, cleaned_data, errors)

        try:
            self.clean(form_state, cleaned_data, errors)
        except ValidationError as e:
            errors[NON_FIELD_ERRORS] = self.error_class(e.messages)

    def is_valid(self, state, context):

        if not state.form_state.is_bound:
            return False

        cleaned_data = {}
        errors = ErrorDict()

        self._validate(state.form_state, cleaned_data, errors)

        state.form_state.cleaned_data = cleaned_data
        state.form_state.errors = errors

        return not bool(errors)

    def clean(self, form_state, cleaned_data, errors):
        pass

    def save(self, state, context):
        pass


class Form(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    "A collection of Fields, plus their associated data."
    # This is a separate class from BaseForm in order to abstract the way
    # self.fields is specified. This class (Form) is the one that does the
    # fancy metaclass stuff purely for the semantic sugar -- it allows one
    # to define a form using declarative syntax.
    # BaseForm itself has no way of designating self.fields.


class FormDisplay(object):

    def __init__(self, form, form_state):
        self.form = form
        self.form_state = form_state

        # The base_fields class attribute is the *class-wide* definition of
        # fields. Because a particular *instance* of the class might want to
        # alter self.fields, we create self.fields here by copying base_fields.
        # Instances should always modify self.fields; they should not modify
        # self.base_fields.
        self.fields = copy.deepcopy(self.form.fields)

    @property
    def add_prefix(self):
        return self.form.add_prefix

    @property
    def add_initial_prefix(self):
        return self.form.add_initial_prefix

    @property
    def auto_id(self):
        return self.form.auto_id

    @property
    def is_bound(self):
        return self.form_state.is_bound

    @property
    def initial(self):
        return self.form_state.initial

    @property
    def data(self):
        return self.form_state.data

    @property
    def files(self):
        return self.form_state.files

    def non_field_errors(self):
        """
        Returns an ErrorList of errors that aren't associated with a particular
        field -- i.e., from Form.clean(). Returns an empty ErrorList if there
        are none.
        """
        return self.form_state.errors.get(NON_FIELD_ERRORS, self.form.error_class())

    def __iter__(self):
        for name in self.fields:
            yield self[name]

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError('Key %r not found in Form' % name)
        return BoundField(self.form, self.form_state, field, name)


class BoundField(object):
    "A Field plus data"

    def __init__(self, form, form_state, field, name):
        self.form = form
        self.form_state = form_state
        self.field = field
        self.name = name
        self.html_name = form.add_prefix(name)
        self.html_initial_name = form.add_initial_prefix(name)
        self.html_initial_id = form.add_initial_prefix(self.auto_id)
        if self.field.label is None:
            self.label = pretty_name(name)
        else:
            self.label = self.field.label
        self.help_text = field.help_text or ''

    def __str__(self):
        """Renders this field as an HTML widget."""
        if self.field.show_hidden_initial:
            return self.as_widget() + self.as_hidden(only_initial=True)
        return self.as_widget()

    def __iter__(self):
        """
        Yields rendered strings that comprise all widgets in this BoundField.

        This really is only useful for RadioSelect widgets, so that you can
        iterate over individual radio buttons in a template.
        """
        for subwidget in self.field.widget.subwidgets(self.html_name, self.value()):
            yield subwidget

    def __len__(self):
        return len(list(self.__iter__()))

    def __getitem__(self, idx):
        return list(self.__iter__())[idx]

    @property
    def errors(self):
        """
        Returns an ErrorList for this field. Returns an empty ErrorList
        if there are none.
        """
        return self.form_state.errors.get(self.name, self.form.error_class())

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """
        Renders the field by rendering the passed widget, adding any HTML
        attributes passed as attrs.  If no widget is specified, then the
        field's default widget will be used.
        """
        if not widget:
            widget = self.field.widget

        if self.field.localize:
            widget.is_localized = True

        attrs = attrs or {}
        auto_id = self.auto_id
        if auto_id and 'id' not in attrs and 'id' not in widget.attrs:
            if not only_initial:
                attrs['id'] = auto_id
            else:
                attrs['id'] = self.html_initial_id

        if not only_initial:
            name = self.html_name
        else:
            name = self.html_initial_name
        return widget.render(name, self.value(), attrs=attrs)

    def as_text(self, attrs=None, **kwargs):
        """
        Returns a string of HTML for representing this as an <input type="text">.
        """
        return self.as_widget(TextInput(), attrs, **kwargs)

    def as_textarea(self, attrs=None, **kwargs):
        "Returns a string of HTML for representing this as a <textarea>."
        return self.as_widget(Textarea(), attrs, **kwargs)

    def as_hidden(self, attrs=None, **kwargs):
        """
        Returns a string of HTML for representing this as an <input type="hidden">.
        """
        return self.as_widget(self.field.hidden_widget(), attrs, **kwargs)

    @property
    def data(self):
        """
        Returns the data for this BoundField, or None if it wasn't given.
        """
        return self.field.widget.value_from_datadict(
            self.form_state.data,
            self.form_state.files,
            self.html_name)

    def value(self):
        """
        Returns the value for this BoundField, using the initial value if
        the form is not bound or the data otherwise.
        """
        if not self.form_state.is_bound:
            data = self.form_state.initial.get(self.name, self.field.initial)
            if callable(data):
                data = data()
        else:
            data = self.field.bound_data(
                self.data, self.form_state.initial.get(self.name, self.field.initial)
            )
        return self.field.prepare_value(data)

    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        """
        Wraps the given contents in a <label>, if the field has an ID attribute.
        contents should be 'mark_safe'd to avoid HTML escaping. If contents
        aren't given, uses the field's HTML-escaped label.

        If attrs are given, they're used as HTML attributes on the <label> tag.

        label_suffix allows overriding the form's label_suffix.
        """
        contents = contents or self.label
        # Only add the suffix if the label does not end in punctuation.
        label_suffix = label_suffix if label_suffix is not None else self.form.label_suffix
        # Translators: If found as last label character, these punctuation
        # characters will prevent the default label_suffix to be appended to the label
        if label_suffix and contents and contents[-1] not in _(':?.!'):
            contents = format_html('{0}{1}', contents, label_suffix)
        widget = self.field.widget
        id_ = widget.attrs.get('id') or self.auto_id
        if id_:
            id_for_label = widget.id_for_label(id_)
            if id_for_label:
                attrs = dict(attrs or {}, **{'for': id_for_label})
            attrs = flatatt(attrs) if attrs else ''
            contents = format_html('<label{0}>{1}</label>', attrs, contents)
        else:
            contents = conditional_escape(contents)
        return mark_safe(contents)

    def css_classes(self, extra_classes=None):
        """
        Returns a string of space-separated CSS classes for this field.
        """
        if hasattr(extra_classes, 'split'):
            extra_classes = extra_classes.split()
        extra_classes = set(extra_classes or [])
        if self.form_state.errors and hasattr(self.form, 'error_css_class'):
            extra_classes.add(self.form.error_css_class)
        if self.field.required and hasattr(self.form, 'required_css_class'):
            extra_classes.add(self.form.required_css_class)
        return ' '.join(extra_classes)

    @property
    def is_hidden(self):
        "Returns True if this BoundField's widget is hidden."
        return self.field.widget.is_hidden

    @property
    def auto_id(self):
        """
        Calculates and returns the ID attribute for this BoundField, if the
        associated Form has specified auto_id. Returns an empty string otherwise.
        """
        auto_id = self.form.auto_id
        if auto_id and '%s' in smart_str(auto_id):
            return smart_str(auto_id) % self.html_name
        elif auto_id:
            return self.html_name
        return ''

    @property
    def id_for_label(self):
        """
        Wrapper around the field widget's `id_for_label` method.
        Useful, for example, for focusing on this field regardless of whether
        it has a single widget or a MultiWidget.
        """
        widget = self.field.widget
        id_ = widget.attrs.get('id') or self.auto_id
        return widget.id_for_label(id_)
