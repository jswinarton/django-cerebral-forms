import django
from django.conf import settings

from cerebral import forms

settings.configure()
django.setup()


class ExampleForm(forms.Form):
    first_name = forms.CharField(
        fill=True, hide=False, requires=[])
    last_name = forms.CharField(
        fill=True, hide=False, requires=[])
    email = forms.CharField(
        fill=True, hide=False, requires=[])
    job_title = forms.CharField(
        hide=True, requires=['email'])
    annual_ad_budget = forms.CharField(
        hide=True, requires=['job_title'])
    comments = forms.CharField(
        fill=False, hide=False, requires=[])


# Data passed to the cerebellum can be from any external source
# that collects user data, such as a database or a CRM like SalesForce.
cerebellum = {
    'first_name': 'Jeremy',
    'last_name': 'Swinarton',
    'email': 'jeremy@swinarton.com',
}

form = ExampleForm(cerebellum=cerebellum)

form.fields.keys()
# ['first_name', 'last_name', 'email', 'job_title', 'comments']

form.initial
# {'first_name': 'Jeremy', 'last_name': 'Swinarton', 'email': 'jeremy@swinarton.com'}


# Let's submit some user data to the form and validate it.
bound_form = ExampleForm({
    'first_name': 'Jeremy',
    'last_name': 'Swinarton',
    'email': 'jeremy@swinarton.com',
    'job_title': 'Web Developer',
    'comments': 'Hi!',
}, cerebellum=cerebellum)
bound_form.is_valid()  # True


# In this example, we've submitted and validated the form, and added its data
# back to our database. Let's create the form again with a new cerebellum.
# This time, the job_title field will be hidden, and we'll be shown the
# annual_ad_budget_field instead.
cerebellum = bound_form.data
progressive_form = ExampleForm(cerebellum=cerebellum)

progressive_form.fields.keys()
# ['first_name', 'last_name', 'email', 'annual_ad_budget', 'comments']

progressive_form.initial
# {'first_name': 'Jeremy', 'last_name': 'Swinarton', 'email': 'jeremy@swinarton.com'}
