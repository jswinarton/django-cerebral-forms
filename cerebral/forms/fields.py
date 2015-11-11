from django import forms as django_forms


class CharField(django_forms.CharField):
    def __init__(self, *args, **kwargs):
        self.hide = kwargs.pop('hide', False)
        self.fill = kwargs.pop('fill', False)
        self.requires = kwargs.pop('requires', [])
        super(CharField, self).__init__(*args, **kwargs)
