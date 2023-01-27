from django.urls import include, path
from rest_framework import routers

from chat import views
from chat.views import MessageViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls),
         name='massages'),
    path('chat/v1', views.chat_view, name='chats'),
    path('chat/v1/<int:sender>/<int:receiver>/', views.message_view,
         name='chat'),
    path('api/v1/messages/<int:sender>/<int:receiver>/', views.message_list,
         name='message-detail'),
    path('api/v1/messages/', views.message_list, name='message-list'),
    ]
