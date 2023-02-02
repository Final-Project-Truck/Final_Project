from django import forms
from survey.models import Survey, Question, Option
from company.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["prompt", "type"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]
