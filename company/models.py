from django.db import models, transaction

from survey.models import Survey, Question, Option, SurveyQuestion


class CompanyQuerySet(models.QuerySet):
    """
    Custom QuerySet for the BaseUsers model.
    """

    def create_multiple(self, objs):
        """
        Create multiple Company instances in one go.

        Args:
            objs (List[BaseUsers]): List of BaseUsers instances to be created.
        """
        for obj in objs:
            obj.save()
        return self

    def delete(self):
        """
        Delete multiple Company instances in one go.

        Also deletes the related Template Survey instances.
        """
        for obj in self:
            obj.delete()
        return super(CompanyQuerySet, self).delete()


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    # override the Model Manager objects
    objects = CompanyQuerySet.as_manager()

    def __str__(self):
        return f'{self.name}'

    @transaction.atomic()
    def save(self, *args, **kwargs):
        """
        Save method for the Company model.
        The decorator @transaction.atomic() ensures that all database
        operations within the method are executed within a single
        transaction. This is important because we want to ensure that all
        operations related to creating or updating the Company and Survey
        models are atomic, meaning that they either all succeed or all fail.
        """
        if self._state.adding:
            super().save(*args, **kwargs)

            title = f"{self.name}'s Template Survey"
            survey = Survey.objects.create(title=title, is_active=False,
                                           company=self)
            questions = [
                {"prompt": f"{self.name}'s Question 1", "type": "cho",
                 "options": [{"text": "True"}, {"text": "False"}]},
                {"prompt": f"{self.name}'s Question 2", "type": "cho",
                 "options": [{"text": "Strongly Agree"}, {"text": "Agree"},
                             {"text": "Neutral"}, {"text": "Disagree"},
                             {"text": "Strongly Disagree"}]},
                {"prompt": f"{self.name}'s Question 3", "type": "txt",
                 "options": []}
            ]
            for question_data in questions:
                question = Question.objects.create(
                    prompt=question_data['prompt'], type=question_data['type'],
                    template_question=True)
                [Option.objects.create(question=question,
                                       text=option_data['text']) for
                 option_data in question_data['options']]
                SurveyQuestion.objects.create(survey=survey, question=question)
            survey.is_active = True
            survey.save()

        else:
            super().save(*args, **kwargs)

    def create_multiple(self, objs):
        self.objects.create_multiple(objs)
        super().bulk_create(objs)

    # @transaction.atomic() #todo do we want to delete the related template
    #  survey when a company is deleted?
    # def delete(self, *args, **kwargs):
    #     template_survey = Survey.objects.get(company=self, creator=None)
    #     template_survey.delete()
    #     super().delete(*args, **kwargs)


class JobPosting(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey("baseuser.CompanyProfile",
                                on_delete=models.CASCADE,
                                related_name='jobs_company')
    description = models.TextField(max_length=300)
    salary = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.job_title}'


class JobPostComment(models.Model):
    post = models.ForeignKey(JobPosting, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey("baseuser.BaseUsers", on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class PostLike(models.Model):
    """
    This model represents a user's like on a job post.
    A user can only like a post once.
    """
    user = models.ForeignKey("baseuser.BaseUsers",
                             on_delete=models.CASCADE,
                             related_name='post_likes')
    """
    A foreign key to the user who liked the post.
    The related name is used to access the user's likes.
    """
    post = models.ForeignKey(JobPosting,
                             on_delete=models.CASCADE,
                             related_name='likes')
    """
    A foreign key to the post that was liked.
    The related name is used to access the likes of a post.
    """
    created = models.DateTimeField(auto_now_add=True)
