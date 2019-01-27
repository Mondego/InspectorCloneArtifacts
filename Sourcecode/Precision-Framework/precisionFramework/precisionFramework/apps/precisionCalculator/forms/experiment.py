from django import forms
from ..models import Experiment, Tool


class ExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        user = request.user
        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.fields['tool'].queryset = Tool.objects.filter(user=user.profile)

    class Meta:
        model = Experiment
        fields = (
            "name",
            'tool',
            "clonepairs",
            )
