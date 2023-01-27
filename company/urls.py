from django.urls import include, path
from rest_framework import routers

from company.views import CompanyAPIViewSet, JobPostCommentAPIViewSet, \
    JobPostingAPIViewSet

router = routers.DefaultRouter()

router.register(r'job_posting', JobPostingAPIViewSet)
router.register(r'job_post_comment', JobPostCommentAPIViewSet)
router.register(r'companies', CompanyAPIViewSet)

urlpatterns = [
    path('', include(router.urls),
         name='companies'),
]
