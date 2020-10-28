from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_framework.routers import DefaultRouter

from . import views
from .views import Follow

app_name = 'users'
router = DefaultRouter()
router.register(r'skills', views.SkillsViewSet)
router.register(r'feed', views.FeedViewSet)
router.register(r'education', views.EducationViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^account/', include('allauth.urls')),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),

    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email,
        name='account_confirm_email'),

    path('follow/<uuid:user_id>/', views.Follow.as_view(), name="follow"),
    path('unfollow/<uuid:user_id>/', views.Unfollow.as_view(), name='unfollow'),
    path('followers/', views.ListFollowers.as_view(), name='followers'),
    path('following/', views.ListFollowing.as_view(), name='following'),
    path('friendrequests/<uuid:user_id>/', views.SendFriendRequest.as_view(), name='send-friend-request'),
    path('friendrequests/accept/<uuid:request_id>/', views.AcceptFriendRequest.as_view(), name='accept-friend-request'),

    path('', include(router.urls)),

]
#    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'user-list'),
#    path('users/<uuid:pk>/', views.UserViewSet.as_view(
#        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name = 'user-detail'),
#    path('experience/', views.ExperienceViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'experience-list'),
#    path('accounts/profile/', views.ProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'profile-list'),
#    path('education/', views.EducationViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'education-list'),
#    path('user/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'User-list'),
#    path('feed/', views.FeedViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'Feed-list'),
#    path('skills/', views.SkillsViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'Skills-list'),

#    path('profile/', views.ProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name = 'profile-list'),
#    path('education/<uuid:pk>/', views.EducationViewSet.as_view(
#        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
#         name = 'education-detail'),
#    path('experience/<uuid:pk>/', views.ExperienceViewSet.as_view(
#        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
#         name = 'experience-detail'),
#    path('profile/<uuid:pk>/', views.ProfileViewSet.as_view(
#        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name = 'profile-detail'),
#    path('feed/<uuid:pk>/', views.FeedViewSet.as_view(
#        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name = 'Feed-detail'),
#    path('skills/<uuid:pk>/', views.SkillsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name = 'Skills-detail'),
