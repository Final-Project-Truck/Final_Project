from django.db import transaction
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsOwner
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from baseuser.models import CompanyProfile
from company.models import JobPosting, Company, JobPostComment
from company.serializers import CompanySerializer, JobPostingSerializer, \
    JobPostCommentSerializer
from survey.models import Survey, Question, Option, SurveyQuestion
from requests.auth import HTTPBasicAuth


class CompanyAPIViewSet(ModelViewSet):
    search_fields = ['name', 'location', 'description']
    filter_backends = (filters.SearchFilter,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            """Create Company"""
            company = Company.objects.create(**serializer.data)

            """Create Company Survey"""
            survey = Survey.objects.create(
                title="Template Survey", is_active=False, company=company)

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

            return Response(CompanySerializer(company).data, status=201)

    def update(self, request, *args, **kwargs):
        company = self.get_object()
        serializer = self.get_serializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.baseuser.user_type == 'com':
            com_profile = CompanyProfile.objects.get(
                base_user_id=request.user.baseuser.id)
            if com_profile.company.id == company.id:
                Company.objects.filter(
                    id=company.id).update(
                    name=serializer.validated_data['name'],
                    location=serializer.validated_data['location'],
                    description=serializer.validated_data['description'])
                return Response('Your company details have been updated',
                                status=201)
            else:
                return Response(
                    'You cannot make changes to other companies')
        elif request.user.is_staff:
            Company.objects.filter(
                id=company.id).update(
                name=serializer.validated_data['name'],
                location=serializer.validated_data['location'],
                description=serializer.validated_data['description'])
            return Response('Company information updated', status=201)
        else:
            return Response(
                'Please contact an administrator to make changes to a company')

    def destroy(self, request, *args, **kwargs):
        chosen_company = self.get_object()
        if request.user.baseuser.user_type == 'com':
            com_profile = CompanyProfile.objects.get(
                base_user_id=request.user.baseuser.id)
            if com_profile.company.id == chosen_company.id:
                self.perform_destroy(chosen_company)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    'You cannot delete companies other than your own')
        elif request.user.is_staff:
            self.perform_destroy(chosen_company)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                'Please contact an administrator to make changes to a company')

    def perform_destroy(self, chosen_company):
        with transaction.atomic():
            chosen_company.delete()


class JobPostingAPIViewSet(ModelViewSet):
    search_fields = ['job_title', 'description', 'company__company__name']
    filter_backends = (filters.SearchFilter,)
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        serializer = JobPostingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_title = serializer.data['job_title']
        description = serializer.data['description']
        salary = serializer.data['salary']

        if request.user.baseuser.user_type == 'com':
            com_profile = CompanyProfile.objects.get(
                base_user_id=request.user.baseuser.id)
            with transaction.atomic():
                job_post = JobPosting.objects.create(
                    job_title=job_title,
                    description=description,
                    salary=salary,
                    company_id=com_profile.company.id,
                )
                job_post.save()
                return Response(JobPostingSerializer(job_post).data,
                                status=201)
        else:
            return Response('Only companies can post jobs')


class JobPostCommentAPIViewSet(ModelViewSet):
    search_fields = ['text',]
    filter_backends = (filters.SearchFilter,)
    queryset = JobPostComment.objects.all()
    serializer_class = JobPostCommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = JobPostCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.data['post']
        text = serializer.data['text']
        date_created = serializer.data['date_created']
        with transaction.atomic():
            new_comment = JobPostComment.objects.create(
                post_id=post,
                text=text,
                date_created=date_created,
                author_id=request.user.baseuser.id)
            new_comment.save()
            return Response(JobPostCommentSerializer(new_comment).data,
                            status=201)


"""Form View"""
basic = HTTPBasicAuth('peter', '12345')


@login_required
def company(request):
    """User can view all companies in the system"""
    companies = requests.get('http://127.0.0.1:8000/api/v1/companies/',
                             auth=basic)
    return render(request, "company_list.html", {"companies": companies})


@login_required
def company_details(request, company_id):
    """Show all company details with button to create survey"""
    specific_company = Company.objects.get(id=company_id)
    context = {
        'company': specific_company,
        'surveys': Survey.objects.filter(company_id=specific_company.id)
    }
    return render(request, 'company_details.html', context)
