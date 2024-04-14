from rest_framework import serializers
from managers.models import Manager


class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()

    class Meta:
        model = Manager
        fields = "__all__"
