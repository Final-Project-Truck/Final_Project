from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from company.forms import CompanyRegistrationForm
from company.models import JobPosting, Company
from company.serializers import CompanySerializer, JobPostingSerializer
from survey.models import Survey, Question, Option, SurveyQuestion


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
            survey = Survey.objects.create(
                title=company.name, is_active=False, company=company)

            """Template Question 1"""
            template_question_1 = Question.objects.create(
                prompt="Question 1", type='cho', template_question=True)
            template_question_1.save()
            template_question_1_option_1 = Option.objects.create(
                question=template_question_1, text="True")
            template_question_1_option_1.save()
            template_question_1_option_2 = Option.objects.create(
                question=template_question_1, text="False")
            template_question_1_option_2.save()
            # related to template question 1

            """Template Question 2"""
            template_question_2 = Question.objects.create(
                prompt="Question 2", type='cho', template_question=True)
            template_question_2.save()
            template_question_2_option_1 = Option.objects.create(
                question=template_question_2, text="Strongly Agree")
            template_question_2_option_1.save()
            template_question_2_option_2 = Option.objects.create(
                question=template_question_2, text="Agree")
            template_question_2_option_2.save()
            template_question_2_option_3 = Option.objects.create(
                question=template_question_2, text="Neutral")
            template_question_2_option_3.save()
            template_question_2_option_4 = Option.objects.create(
                question=template_question_2, text="Disagree")
            template_question_2_option_4.save()
            template_question_2_option_5 = Option.objects.create(
                question=template_question_2, text="Strongly Disagree")
            template_question_2_option_5.save()

            """Template Question 3"""
            template_question_3 = Question.objects.create(
                prompt="Question 3", type='txt', template_question=True)
            template_question_3.save()

            """Combine Template Questions with Company Survey"""
            survey_question_1 = SurveyQuestion.objects.create(
                survey=survey, question=template_question_1)
            survey_question_1.save()
            survey_question_2 = SurveyQuestion.objects.create(
                survey=survey, question=template_question_2)
            survey_question_2.save()
            survey_question_3 = SurveyQuestion.objects.create(
                survey=survey, question=template_question_3)
            survey_question_3.save()

            """Change is_active to True to activate survey"""
            Survey.objects.filter(pk=survey.id).update(is_active=True)
            survey.save()

            return Response(CompanySerializer(company).data, status=201)


class JobPostingAPIViewSet(ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer


def company_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CompanyRegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'])
                company = form.save(commit=False)
                company.django_user = user
                company.save()
                messages.success(request, 'Company registered successfully')
                send_mail(
                    'Register Completed',  # Change your Subject
                    'Thank you for joining our Website',  # Change your message

                    'tryharderbruhhh@gmail.com',  # Put the email your going
                    # to use
                    [user.email],
                    fail_silently=False
                )
                return redirect('company_login')
        else:
            form = CompanyRegistrationForm()
        return render(request, 'company_register.html', {'form': form})


def company_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username,
                                password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,
                               'Company email OR password is incorrect')

        context = {}
        return render(request, 'company_login.html', context)


def company_logout(request):
    logout(request)
    return redirect('company_login')
