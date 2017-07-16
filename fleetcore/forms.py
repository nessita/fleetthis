from django import forms


class DeltaForm(forms.Form):

    delta = forms.DecimalField(decimal_places=2)
