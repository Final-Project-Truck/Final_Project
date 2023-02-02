from django.db import transaction
from django.db.models import Exists, OuterRef, Q, Count
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsOwner
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from baseuser.models import CompanyProfile
from company.models import JobPosting, Company, JobPostComment, PostLike
from company.serializers import CompanySerializer, JobPostingSerializer, \
    JobPostCommentSerializer, PostLikeSerializer
from survey.models import Survey, Question, Option, SurveyQuestion
from survey.serializers import SurveySerializer


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
            title = f"{company.name}'s Template Survey "
            """Create Company Survey"""
            survey = Survey.objects.create(
                title=title, is_active=False, company=company)
            question_1 = f"{company.name}'s Question 1"
            question_2 = f"{company.name}'s Question 2"
            question_3 = f"{company.name}'s Question 3"

            text_1 = f"{question_1} True"
            text_2 = f"{question_1} False"
            text_3 = f"{question_2} Strongly Agree"
            text_4 = f"{question_2} Agree"
            text_5 = f"{question_2} Neutral"
            text_6 = f"{question_2} Disagree"
            text_7 = f"{question_2} Strongly Disagree"

            """Template Question 1"""
            template_question_1 = Question.objects.create(
                prompt=question_1, type='cho', template_question=True)
            template_question_1.save()
            template_question_1_option_1 = Option.objects.create(
                question=template_question_1, text=text_1)
            template_question_1_option_1.save()
            template_question_1_option_2 = Option.objects.create(
                question=template_question_1, text=text_2)
            template_question_1_option_2.save()
            # related to template question 1

            """Template Question 2"""
            template_question_2 = Question.objects.create(
                prompt=question_2, type='cho', template_question=True)
            template_question_2.save()
            template_question_2_option_1 = Option.objects.create(
                question=template_question_2, text=text_3)
            template_question_2_option_1.save()
            template_question_2_option_2 = Option.objects.create(
                question=template_question_2, text=text_4)
            template_question_2_option_2.save()
            template_question_2_option_3 = Option.objects.create(
                question=template_question_2, text=text_5)
            template_question_2_option_3.save()
            template_question_2_option_4 = Option.objects.create(
                question=template_question_2, text=text_6)
            template_question_2_option_4.save()
            template_question_2_option_5 = Option.objects.create(
                question=template_question_2, text=text_7)
            template_question_2_option_5.save()

            """Template Question 3"""
            template_question_3 = Question.objects.create(
                prompt=question_3, type='txt', template_question=True)
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

    @action(detail=True, methods=['get'])
    def get_active_surveys(self, request, pk=None):
        company = self.get_object()

        surveys = Survey.objects.filter(company=company, is_active=True)

        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class JobPostingAPIViewSet(ModelViewSet):
    search_fields = ['job_title', 'description', 'company__company__name']
    filter_backends = (filters.SearchFilter,)
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        check = Exists(PostLike.objects.filter(user=self.request.user.baseuser,
                                               post_id=OuterRef('pk')))
        return JobPosting.objects.annotate(is_liked=check).\
            order_by('job_title')

    def create(self, request, *args, **kwargs):
        serializer = JobPostingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_title = serializer.data['job_title']
        description = serializer.data['description']
        salary = serializer.data['salary']

        if request.user.baseuser.user_type == 'com':
            com_profile = CompanyProfile.objects.get(  # todo check who have
                # made it filter
                base_user_id=request.user.baseuser.id)
            with transaction.atomic():
                if com_profile:
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
                    return Response(
                        'Please create Company profile to post a job')
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


class PostLikeAPIViewSet(ModelViewSet):
    """
    A ViewSet for handling the CRUD operations for a user's post likes.
    """
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Only return the post likes for the authenticated user.
        """
        user = self.request.user.baseuser
        return PostLike.objects.filter(Q(user=user))

    def get(self, request, pk):
        """
        Retrieve the like count for a specific job post.
        """
        job_post = JobPosting.objects.filter(pk=pk).annotate(
            like_count=Count('likes'))
        serializer = self.serializer_class(job_post, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new post like.
        Will return a 304 status code if the post is already liked by the user.
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            liker = request.user.baseuser
            post = serializer.validated_data.get('post')
            if PostLike.objects.filter(user=liker, post=post).exists():
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            serializer.save(user=liker, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Handle the update of a post like.
        Will return a 304 status code if the post is already liked by the user.
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            liker = request.user.baseuser
            post = serializer.validated_data.get('post')
            if PostLike.objects.filter(user=liker, post=post).exclude(
                    pk=instance.pk).exists():
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            serializer.save(user=liker, post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handle the deletion of a post like.
        Will return a 403 status code if the authenticated user is not the one
        who created the like
        """
        instance = self.get_object()
        if instance.user != request.user.baseuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
