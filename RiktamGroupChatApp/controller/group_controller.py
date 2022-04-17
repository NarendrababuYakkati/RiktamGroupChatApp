from RiktamGroupChatApp.serializers import *

class GroupController:
    def __init__(self):
        pass

    def get_group_users(self, user_id):
        serializer = RgcaGroupMembers.objects.filter(user_id=user_id, is_active_member=True).values()
        data = RgcaGroupSerializer(serializer)
        return data