"""frss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from frssapi.views.auth import register_user, login_user

from frssapi.views.analytics import AnalyticsView
from frssapi.views import AnswerView, QuestionView, SummaryView
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'answers', AnswerView, 'answer')
router.register(r'questions', QuestionView, 'question')
router.register(r'summary', SummaryView, 'summary')
router.register(r'analytics', AnalyticsView, 'analytics')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')), 
    ]
