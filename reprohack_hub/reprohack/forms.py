from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML, Field
# from leaflet.forms.widgets import LeafletWidget

from .models import Event, Paper, Review

# -------- Event -------- #
LEAFLET_WIDGET_ATTRS = {
    'DEFAULT_CENTER': (6.0, 45.0),
    'DEFAULT_ZOOM': 5,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
}


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['submission_date', 'creator', ]
        # widgets = {'geom': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator')
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit event'))
        self.helper.layout = Layout(
            'title',
            'host',
            Row(
                Column('start_time', css_class='form-group col-md-4 mb-0'),
                Column('end_time', css_class='form-group col-md-4 mb-0'),
                Column('time_zone', css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            ),
            # 'venue',
            'venue_description',
            'address1',
            'address2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('postcode', css_class='form-group col-md-3 mb-0'),
                Column('country', css_class='form-group col-md-3 mb-0'),
            ),
            'registration_url',
            # 'geom',
        )


# -------- Paper -------- #
class PaperForm(ModelForm):
    class Meta:
        model = Paper
        exclude = ['submission_date', 'creator', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PaperForm, self).__init__(*args, **kwargs)
        # self.email = self.cleaned_data['email']

        # self.fields['authorship'].label = "I am the corresponding author"
        # self.fields['contact'].label = "I can be contacted by participants"

        # self.fields['feedback'].label = "I wish to received feedback on reproductions"
        self.fields['public'].label = "I wish to receive feedback on reproductions"
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit paper'))
        self.helper.layout = Layout(
            HTML('<h2>Paper details<h2>'),
            'title',
            'citation_txt',
            'citation_bib',
            'doi',
            'description',
            'why',
            'focus',
            Fieldset("Links to Resources",
                     Row(
                         Column('paper_url', css_class='form-group col-md-6 mb-0'),
                         Column('data_url',  css_class='form-group col-md-6 mb-0'),
                         css_class='form-row',
                     ),
                     Row(
                         Column('code_url', css_class='form-group col-md-6 mb-0'),
                         Column('extra_url', css_class='form-group col-md-6 mb-0'),
                         css_class='form-row',
                     ),
                     ),
            Field('tools', label="Useful Software Skills"),
            HTML('<h3>Submitter contact details<h3>'),
            Row(
                Column(css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            ),
            Fieldset("Authorship details",
                     # Row(
                     #     Column('authorship', label="I am corresponding author",
                     #            css_class='form-group col-md-6 mb-0'),
                     #     Column('author_first_name',
                     #            css_class='form-group col-md-3 mb-0'),
                     #     Column('author_last_name',
                     #            css_class='form-group col-md-3 mb-0'),
                     #     Column('author_email',
                     #            css_class='form-group col-md-6 mb-0'),
                     #     css_class='form-row',
                     # ),
                     Row(
                         Column('public', label="Feedback can be published",
                                css_class='form-group col-md-6 mb-0'),
                         css_class='form-row',
                     ),
                     ),
        )

    def clean(self):
        authorship = self.cleaned_data.get('authorship')

        if authorship:
            self.cleaned_data['author_user'] = self.user
        else:
            self.cleaned_data['author_user'] = ""
            self.fields_required(['author_first_name'])
            self.fields_required(['author_last_name'])
            self.fields_required(['author_email'])
        return self.cleaned_data

    def fields_required(self, fields):
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)


class ReviewForm(ModelForm):

    """A form to review papers."""

    class Meta:
        model = Review
        exclude = ['reviewers', ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit review'))
