# -*- coding: utf-8 -*-
from django import forms
from .models import Institution
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import FormHorizontalMixin
from dal import autocomplete
from ..teryt.models import JST
from django.utils.translation import ugettext as _
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class InstitutionForm(UserKwargModelFormMixin, FormHorizontalMixin, forms.ModelForm):
    # TODO: Split region,voivodeship,county into forms.MultiWidget
    voivodeship = forms.ModelChoiceField(
        label=_("Voivodeship"),
        required=False,
        queryset=JST.objects.voivodeship().all(),
        widget=autocomplete.ModelSelect2(url='teryt:voivodeship-autocomplete')
    )
    county = forms.ModelChoiceField(
        label=_("County"),
        required=False,
        queryset=JST.objects.county().all(),
        widget=autocomplete.ModelSelect2(url='teryt:county-autocomplete',
                                         forward=['voivodeship'],
                                         )
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            instance = kwargs.get('instance')
            kwargs['initial'] = kwargs.get('initial', {})
            if instance.region.parent:
                kwargs['initial']['county'] = instance.region.parent.pk
                if instance.region.parent.parent:
                    kwargs['initial']['voivodeship'] = instance.region.parent.parent.pk

        super(InstitutionForm, self).__init__(*args, **kwargs)
        button_label = _('Update') if self.instance.pk else _("Save")
        self.instance.user = self.user
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Fieldset(
                _('Identification'),
                'name',
                'regon',
                'krs',
            ),
            Fieldset(
                _('Location'),
                'voivodeship',
                'county',
                'region',
            ),
            Fieldset(
                _('Monitorings'),
                'monitorings',
            ),
            ButtonHolder(
                Submit('submit', button_label, css_class='button white')
            )
        )

    class Meta:
        model = Institution
        fields = ['name', 'regon', 'krs', 'region', 'monitorings']
        widgets = {
            'region': autocomplete.ModelSelect2(url='teryt:community-autocomplete',
                                                forward=['county']),
            'monitorings': autocomplete.ModelSelect2Multiple(url='monitorings:autocomplete')
        }
