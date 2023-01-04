from django.db import models
from django.utils import timezone

from baseuser.models import BaseUsers
from company.models import Company

# from django.contrib.auth.models import User

question_type = [('txt', 'Text'),
                 ('cho', 'Choice')]


# todo create template survey?
class Survey(models.Model):
    """A survey created by a user."""

    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(BaseUsers, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    """A question in a survey"""
# Todo check for manytomany vs foreignkey--> Mathias suggested having it as manytomany
    prompt = models.CharField(max_length=128)
    type = models.CharField(max_length=3, choices=question_type)

    def __str__(self):
        return f'{self.prompt}'


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='survey_question')


class Option(models.Model):
    """A multi-choice option available as a part of a survey question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_options')
    text = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.text}'


class Submission(models.Model):
    """A set of answers a survey's questions."""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_submission')
    created_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)
    submitter = models.ForeignKey(BaseUsers, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.submitter} made submission to {self.survey}'


class AnswerChoice(models.Model):
    """An answer a survey's choice questions."""

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='choice_submission')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers_choice')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='answer_options')



class AnswerText(models.Model):
    """An answer a survey's text questions."""
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='text_submission')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers_text')
    comment = models.TextField()

    def __str__(self):
        return f'{self.submission}'
