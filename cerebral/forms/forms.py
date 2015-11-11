from django import forms as django_forms


EMPTY_VALUES = (None, '')


class Form(django_forms.Form):
    def __init__(self, *args, **kwargs):
        self.cerebellum = kwargs.pop('cerebellum', None)
        super(Form, self).__init__(*args, **kwargs)
        self._strip_fields()
        self._add_fill_data()

    def _strip_fields(self):
        for key in self.fields.keys():
            if key not in self.visible_fields:
                self.fields.pop(key, None)

    def _add_fill_data(self):
        self.initial.update(self.filled_fields)

    def field_is_visible(self, field_name):
        '''
        Given a field name as a string, checks if the field
        is visible. Returns a boolean.
        '''
        field = self.fields.get(field_name)

        if field is None:
            return False

        if field.hide:
            if field_name in self.cerebellum:
                return False

        for required_field_name in field.requires:
            if (
                self.cerebellum.get(required_field_name) in
                EMPTY_VALUES
            ):
                return False

        return True

    def field_value(self, field_name):
        field = self.fields.get(field_name)
        value = self.cerebellum.get(field_name)

        if field.fill and value not in EMPTY_VALUES:
            return value
        return None

    @property
    def visible_fields(self):
        '''
        A list of all fields that are visible on this form.
        TODO: change nomenclature. "visible" is used to describe
        the state of HTML form elements in the DOM.
        This could be confusing
        '''
        return [f for f in self.fields.keys() if self.field_is_visible(f)]

    @property
    def filled_fields(self):
        '''
        Returns a dict of fields that should be filled by cerebellum data.
        '''
        filled_fields = {}
        for field_name in self.fields.keys():
            value = self.field_value(field_name)
            if value not in EMPTY_VALUES:
                filled_fields[field_name] = value
        return filled_fields
