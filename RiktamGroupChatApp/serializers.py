from rest_framework import serializers
from .models import *

class RgcaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RgcaGroups
        fields = "__all__"

class RgcaGroupMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RgcaGroupMembers
        fields = ["group_id", "user_id", "is_admin", "is_active_member","added_at"]

class RgcaGroupMessagesMappingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RgcaGroupMessagesMappings
        fields = "__all__"