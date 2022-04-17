from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login_user', views.UserLogin.as_view(), name = "login_user"),
    path('logout_user', views.UserLogout.as_view(), name = "logout_user"),
    # path('delete_group/<group_id>', views.DeleteGroup.as_view(), name = "delete_group"),
    path('get_groups', login_required(views.GetUserGroups.as_view(), login_url='/login_user'), name ='get_groups'),
    path('create_group', login_required(views.CreateGroup.as_view(), login_url='/login_user'), name = 'create_group'),
    path('get_group_members/<group_id>', login_required(views.GetGroupMembers.as_view(), login_url='/login_user'), name= 'get_group_members'),
    path('delete_group/<group_id>', login_required(views.DeleteGroup.as_view(), login_url='/login_user')),
    path("add_member", login_required(views.AddMembersToGroup.as_view(), login_url='/login_user'), name = 'add_member'),
    path('add_message', login_required(views.AddGroupMessage.as_view(),login_url='/login_user'), name = 'add_message')

]