from django.db import models

# Create your models here.

class RgcaGroups(models.Model):
    group_name =models.CharField(max_length=255, blank=True, null=True)
    group_desc = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    create_at = models.BigIntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.BigIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        db_table ="rgca_groups"

class RgcaGroupMembers(models.Model):
    group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active_member = models.BooleanField(default=True)
    added_at = models.BigIntegerField(blank=True, null=True)
    added_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "rgca_group_members"

class RgcaGroupMessges(models.Model):
    group_id = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    sender_id = models.IntegerField(blank=True, null=True)
    added_at = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = "rgca_group_messages"

class RgcaGroupMessagesMappings(models.Model):
    message_id = models.IntegerField(blank=True, null=True)
    receiver_id = models.IntegerField(blank=True, null=True)
    received_at = models.BigIntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    is_liked = models.BooleanField(default=False)


    class Meta:
        db_table = "rgca_group_messages_mappings"


