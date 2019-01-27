from django import forms

class ExperimentActionForm(forms.Form):
    CHOICES = [(1, 'True Positive'), (0, 'False Positive')]
    CLONE_TYPES = [(2, "Type 2"), (3, "Type 3"), (4, "Type 4")]
    vote = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=True)
    clone_type = forms.MultipleChoiceField(choices=CLONE_TYPES, widget=forms.CheckboxSelectMultiple, required=False)
    explanation = forms.CharField(max_length=4000, widget=forms.Textarea(attrs={'rows':2,'cols':40}), required=False)


    def __init__(self, experiment=None,*args, **kwargs):
        request = kwargs.pop("request")
        self.experiment = experiment
        self.user = request.user
        super(ExperimentActionForm, self).__init__(*args, **kwargs)



