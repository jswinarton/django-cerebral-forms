from django import forms as django_forms


EMPTY_FIELD_VALUES = (None, '')


class Form(django_forms.Form):
    def __init__(self, *args, **kwargs):
        self.cerebellum = kwargs.pop('cerebellum', None)
        super(Form, self).__init__(*args, **kwargs)
        self._strip_fields()
        self._add_fill_data()

    @property
    def visible_fields(self):
        '''
        A list of all fields that are visible on this form.
        '''
        return [f for f in self.fields.keys() if self.field_is_visible(f)]

    def field_is_visible(self, field_name):
        '''
        Given a field name as a string,
        checks if the field is visible on the field.
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
                EMPTY_FIELD_VALUES
            ):
                return False

        return True

    @property
    def filled_fields(self):
        pass
        return [f for f in self.fields.keys() if self.field_is_filled(f)]

    def field_is_filled(self, field_name):
        field = self.fields.get(field_name)

        if (
            field.fill and
            self.cerebellum.get(field_name) not in EMPTY_FIELD_VALUES
        ):
            return True
