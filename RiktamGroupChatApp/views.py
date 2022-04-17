from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
# from .forms import SignUpForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.shortcuts import render, redirect
from django.views import View
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
# from django.core import serializers
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status


import time, json
# from .models import *
from .serializers import *
from RiktamGroupChatApp.controller.group_controller import GroupController
# Create your views here.

class UserLogin(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('get_groups')
            else:
                messages.info(request, 'Invalid Username or Password')
                return redirect('login_user')
        except Exception as e:
            raise e

class GetUserGroups(View):
    def get(self, request):
        try:
            user_id = request.user.id
            print(user_id)
            serializer = RgcaGroupMembers.objects.filter(user_id=user_id, is_active_member=True).values()
            data = RgcaGroupSerializer(serializer, many=True)
            print(data.data)
            context = {
                "data":data.data
            }
            print(context)
            return render(request, 'groups.html', context=context)
        except Exception as e:
            raise e

class CreateGroup(APIView):
    def post(self, request):
        try:
            group_data = {}
            member_data = {}
            fields = request.data
            fields['created_user_id'] = request.user.id
            if 'group_name' not  in fields.keys():
                return Response({"status:":"fail", "msg":"Please provide group name"})

            print(type(fields))
            if 'group_desc' in fields.keys():
                print('came')
                group_data['group_desc'] = fields['group_desc']
            group_data['group_name'] = fields['group_name']
            group_data['created_by'] = fields['created_user_id']
            group_data['create_at'] = int(time.time())

            group = RgcaGroups.objects.create(**group_data)
            group_details = RgcaGroups.objects.filter(id=group.id).values().get()
            print(group_details)

            member_data['group_id'] = group.id
            member_data['user_id'] = fields['created_user_id']
            member_data['is_admin'] = True
            member_data['added_at'] = int(time.time())
            RgcaGroupMembers.objects.create(**member_data)

            data = {"status":"success", "data":group_details}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e

class GetGroupMembers(APIView):
    def get(self, request, group_id):
        try:
            requester_id = request.user.id
            is_group_exist = RgcaGroups.objects.filter(id=group_id, is_deleted=False).count()
            if is_group_exist > 0:
                is_group_member = RgcaGroupMembers.objects.filter(group_id=group_id, user_id=requester_id, is_active_member = True).count()
                if is_group_member > 0:
                    serializer = RgcaGroupMembers.objects.filter(group_id = group_id, is_active_member=True).values()
                    print(serializer)
                    data = RgcaGroupMembersSerializer(serializer, many=True)
                    print(data.data)
                    return Response(data.data, status.HTTP_200_OK)
                else:
                    return Response({"status": "fail", "data": "You're not a member"})
            else:
                return Response({"status": "fail", "data": "Invalid group"})
        except Exception as e:
            raise e

class DeleteGroup(APIView):
    def put(self, request, group_id):
        try:
            requester_id = request.user.id
            is_group_exists = RgcaGroups.objects.filter(id = group_id, is_deleted=False).count()
            print(is_group_exists)

            if is_group_exists > 0:
                is_group_admin = RgcaGroupMembers.objects.filter(group_id = group_id, user_id = requester_id, is_admin = True).count()
                print(is_group_admin)
                if  is_group_admin > 0:
                    RgcaGroups.objects.filter(id = group_id).update(is_deleted = True)
                    return Response({"status":"success", "data":"Group deleted successfully"})
                else:
                    return Response({"status": "fail", "data": "You're not an admin"})

            else:
                return Response({"status": "success", "data": "Invalid group"})
        except Exception as e:
            raise e
class AddMembersToGroup(APIView):
    def post(self, request):
        fields = request.data
        member_data = {}
        requester_id = request.user.id

        if "group_id" not in fields.keys() or len(fields['group_id']) == 0:
            return Response({"status": "fail", "data": "Please provide group_id"})

        if "email" not in fields.keys() or len(fields['email']) == 0:
            return Response({"status": "fail", "data": "Please provide email to add the user"})

        user_data = get_user_model().objects.filter(email=fields['email'])
        is_group_exist = RgcaGroups.objects.filter(id = fields['group_id'], is_deleted=False).count()
        is_group_admin = RgcaGroupMembers.objects.filter(group_id=fields['group_id'], user_id=requester_id, is_admin=True).count()

        if is_group_exist > 0:
            if is_group_admin > 0:
                if user_data.count() > 0:
                    u_data = user_data.values('id', 'username')
                    print(user_data)

                    member_data['group_id'] = fields['group_id']
                    member_data['user_id'] = u_data['id']
                    member_data['added_at'] = int(time.time())
                    member_data['added_by'] = requester_id
                    RgcaGroupMembers.objects.create(**member_data)
                    return Response({"status": "success", "data": "User added successfully"})
                else:
                    return Response({"status": "fail", "data": "User is not registered to add"})
            else:
                return Response({"status": "fail", "data": "Your'e not an admin to add "})
        else:
            return Response({"status": "fail", "data": "Invalid group"})

class GroupSearch(APIView):
    def get(self, request):
        pass

class AddGroupMessage(APIView):
    def post(self, request):
        try:
            fields = request.data
            message_data = {}
            requester_id = request.user.id

            if "group_id" not in fields.keys() or len(fields['group_id']) == 0:
                return Response({"status": "fail", "data": "Please provide group_id"})

            if "message" not in fields.keys() or len(fields['message']) == 0:
                return Response({"status": "fail", "data": "Please provide your message"})

            is_group_exist = RgcaGroups.objects.filter(id=fields['group_id'], is_deleted=False).count()
            is_group_member = RgcaGroupMembers.objects.filter(group_id=fields['group_id'], user_id=requester_id,
                                                              is_active_member=True).count()

            print(is_group_exist)
            print(is_group_member)
            if is_group_exist > 0:
                if is_group_member > 0:
                    message_data['group_id'] = fields['group_id']
                    message_data['message'] = fields['message']
                    message_data['sender_id'] = requester_id
                    message_data['added_at'] = int(time.time())

                    message = RgcaGroupMessges.objects.create(**message_data)
                    serializer = RgcaGroupMembers.objects.filter(group_id=fields['group_id'], is_active_member=True).values()
                    print(serializer)
                    data = RgcaGroupMembersSerializer(serializer, many=True)

                    msg_mappings_data = {}
                    all_members_data = data.data
                    for mem in range(len(all_members_data)):
                        msg_mappings_data['message_id'] = message.id
                        msg_mappings_data['receiver_id'] =  all_members_data[mem]['user_id']
                        msg_mappings_data['group_id'] = all_members_data[mem]['group_id']
                        msg_mappings_data['received_at'] = int(time.time())
                        RgcaGroupMessagesMappings.objects.create(**msg_mappings_data)

                    return Response({"status": "success", "data": "Message_added_successfully"})
                else:
                    return Response({"status": "fail", "data": "Your'e not a group_memver to add message"})
            else:
                return Response({"status": "fail", "data": "Invalid group"})

        except Exception as e:
            raise e

class GetUserGroupMessages(APIView):
    def get(self, request, group_id):
        try:
            requester_id = request.user.id
            is_group_exist = RgcaGroups.objects.filter(id=group_id, is_deleted=False).count()
            is_group_member = RgcaGroupMembers.objects.filter(group_id=group_id, user_id=requester_id,
                                                              is_active_member=True).count()
            if is_group_exist > 0:
                if is_group_member > 0:
                    serializer = RgcaGroupMessagesMappings.objects.filter(group_id=group_id, receiver_id=requester_id)
                    data = RgcaGroupMessagesMappingsSerializer(serializer, many=True)
                    return Response(data.data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "fail", "data": "Your'e not a group_memver to add message"})
            else:
                return Response({"status": "fail", "data": "Invalid group"})
        except Exception as e:
            raise e

class LikeMessage(APIView):
    def put(self, request):
        try:
            requester_id = request.user.id
            fields = request.data

            if "group_id" not in fields.keys() or len(fields['group_id']) == 0:
                return Response({"status": "fail", "data": "Please provide group_id"})

            if "message_id" not in fields.keys() or len(fields['message_id']) == 0:
                print(fields)
                return Response({"status": "fail", "data": "Please provide your message"})

            is_group_exist = RgcaGroups.objects.filter(id=fields['group_id'], is_deleted=False).count()
            is_group_member = RgcaGroupMembers.objects.filter(group_id=fields['group_id'], user_id=requester_id,
                                                              is_active_member=True).count()
            if is_group_exist > 0:
                if is_group_member > 0:
                    RgcaGroupMessagesMappings.objects.filter(group_id=fields['group_id'], receiver_id=requester_id, message_id=fields['message_id']).update(is_liked = True)
                    return Response({"status": "success", "data": "message liked"})
                else:
                    return Response({"status": "fail", "data": "Your'e not a group_memver to add message"})
            else:
                return Response({"status": "fail", "data": "Invalid group"})
        except Exception as e:
            raise e


class UserLogout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login_user')

