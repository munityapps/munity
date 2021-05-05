from acl.serializers import GroupRoleSerializer
from base.serializers import ModelSerializerWithFields
from groups.models import Group
from rest_framework import serializers


class GroupSerializer(ModelSerializerWithFields):
    class Meta:
        model = Group
        exclude = ["groups"]

    user_role_in_group = serializers.SerializerMethodField()
    ids = serializers.SerializerMethodField()

    def get_user_role_in_group(self, group):
        try:
            user_group_role = (
                group.group_memberships.only("group_role").get(user=self.context["request"].user).group_role
            )
        except:  # NOQA
            return None
        else:
            serializer = GroupRoleSerializer(user_group_role)
            return serializer.data

    def get_ids(self, group):
        ids = [group.pk for group in group.get_all_groups()]
        return ids
