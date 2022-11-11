from django.db import models

scale = [('5', 'Very Good'),
         ('4', 'Good'),
         ('3', 'Neutral'),
         ('2', 'Poor',),
         ('1', 'Very Poor'),
         ]


class SurveyQuestions(models.Model):
    questions = models.TextField()


class TemplateSurvey(models.Model):
    answer_1 = models.CharField(max_length=1, choices=scale, default='3')
    answer_2 = models.CharField(max_length=1, choices=scale, default='3')
    answer_3 = models.CharField(max_length=1, choices=scale, default='3')
    answer_4 = models.CharField(max_length=1, choices=scale, default='3')
    answer_5 = models.CharField(max_length=1, choices=scale, default='3')


# class Survey(models.Model):
#     Q1 = models.ForeignKey(SurveyQuestions)