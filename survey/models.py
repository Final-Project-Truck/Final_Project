from django.db import models
from baseuser.models import BaseUsers
from company.models import Company

scale = [('5', 'Very Good'),
         ('4', 'Good'),
         ('3', 'Neutral'),
         ('2', 'Poor',),
         ('1', 'Very Poor'),
         ('0', 'Not Applicable'),
         ]

question_type = [('txt', 'Text'),
                 ('scl', 'Scale'),
                 # ('ten', 'Tenure')
                ]


class SurveyQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=3, choices=question_type)
    question = models.TextField()

    def __str__(self):
        return f'{self.question}'


class SurveyAnswer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.OneToOneField(SurveyQuestion, on_delete=models.CASCADE)
    scale_answer = models.CharField(max_length=1, choices=scale, null=True)
    comment = models.TextField(null=True)


class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUsers, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    defunct_company = models.CharField(max_length=100)
    questions = models.ManyToManyField(SurveyQuestion)
    answers = models.ManyToManyField(SurveyAnswer)
