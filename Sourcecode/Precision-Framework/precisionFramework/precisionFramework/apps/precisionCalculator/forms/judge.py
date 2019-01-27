from django import forms
from ..models import Judge


class JudgeForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)


    def __init__(self, experiment=None, *args, **kwargs):
        request = kwargs.pop("request")
        self.experiment = experiment
        self.user = request.user
        super(JudgeForm, self).__init__(*args, **kwargs)
