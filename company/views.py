from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from company.models import Company, JobPosting
from company.serializers import CompanySerializer, JobPostingSerializer
from survey.models import Survey, Question, Option, SurveyQuestion
from .forms import UserRegistrationForm, CompanyRegistrationForm

class CompanyAPIViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            """Create Company"""
            company = Company.objects.create(**serializer.data)

            """Create Company Survey"""
            survey = Survey.objects.create(title=company.name, is_active=False, company=company)


            """Template Question 1"""
            template_question_1 = Question.objects.create(prompt="Question 1", type='cho', template_question=True)
            template_question_1.save()
            template_question_1_option_1 = Option.objects.create(question=template_question_1, text="True")
            template_question_1_option_1.save()
            template_question_1_option_2 = Option.objects.create(question=template_question_1, text="False")
            template_question_1_option_2.save()
            # related to template question 1

            """Template Question 2"""
            template_question_2 = Question.objects.create(prompt="Question 2", type='cho', template_question=True)
            template_question_2.save()
            template_question_2_option_1 = Option.objects.create(question=template_question_2, text="Strongly Agree")
            template_question_2_option_1.save()
            template_question_2_option_2 = Option.objects.create(question=template_question_2, text="Agree")
            template_question_2_option_2.save()
            template_question_2_option_3 = Option.objects.create(question=template_question_2, text="Neutral")
            template_question_2_option_3.save()
            template_question_2_option_4 = Option.objects.create(question=template_question_2, text="Disagree")
            template_question_2_option_4.save()
            template_question_2_option_5 = Option.objects.create(question=template_question_2, text="Strongly Disagree")
            template_question_2_option_5.save()

            """Template Question 3"""
            template_question_3 = Question.objects.create(prompt="Question 3", type='txt', template_question=True)
            template_question_3.save()

            """Combine Template Questions with Company Survey"""
            survey_question_1 = SurveyQuestion.objects.create(survey=survey, question=template_question_1)
            survey_question_1.save()
            survey_question_2 = SurveyQuestion.objects.create(survey=survey, question=template_question_2)
            survey_question_2.save()
            survey_question_3 = SurveyQuestion.objects.create(survey=survey, question=template_question_3)
            survey_question_3.save()

            """Change is_active to True to activate survey"""
            Survey.objects.filter(pk=survey.id).update(is_active=True)
            survey.save()

            return Response(CompanySerializer(company).data, status=201)


class JobPostingAPIViewSet(ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer


def register(request):
    if request.method == 'POST':
        if 'company_submit' in request.POST:
            form = CompanyRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                company = form.save(commit=False)
                company.user = user
                company.save()
                return redirect('login')
        else:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
    else:
        user_form = UserRegistrationForm()
        company_form = CompanyRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form, 'company_form': company_form})