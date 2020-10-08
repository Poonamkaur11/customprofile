from allauth.account import views
from allauth.account.views import confirm_email, PasswordResetView
from django.conf.urls import url
from django.urls import path, include, re_path
from django.contrib import admin
from rest_auth.registration.views import VerifyEmailView
from . import views

from .views import mail

app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view(), name = 'user-list'),
    path('users/<uuid:pk>/', views.UserDetail.as_view(), name = 'user-detail'),
    path('experience/', views.ExperienceList.as_view(), name = 'experience-list'),
    path('accounts/profile/', views.ProfileList.as_view(), name = 'profile-list'),
    path('education/', views.EducationList.as_view(), name = 'education-list'),
    path('user/', views.UserList.as_view(), name = 'User-list'),
    path('feed/', views.FeedList.as_view(), name = 'Feed-list'),
    path('skills/', views.SkillsList.as_view(), name = 'Skills-list'),

    path('profile/', views.ProfileList.as_view(), name = 'profile-list'),
    path('education/<uuid:pk>/', views.EducationDetail.as_view(), name = 'education-detail'),
    path('experience/<uuid:pk>/', views.ExperienceDetail.as_view(), name = 'experience-detail'),
    path('profile/<uuid:pk>/', views.ProfileDetail.as_view(), name = 'profile-detail'),
    path('feed/<uuid:pk>/', views.FeedDetail.as_view(), name = 'Feed-detail'),
    path('skills/<uuid:pk>/', views.SkillsDetail.as_view(), name = 'Skills-detail'),
    path('account/', include('allauth.urls')),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
   # url(r'^account/', include('allauth.urls')),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name = 'account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name = 'account_confirm_email'),

    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),

]
