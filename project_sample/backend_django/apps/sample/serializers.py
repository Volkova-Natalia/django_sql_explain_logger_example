from rest_framework.serializers import ModelSerializer

from .models import People


class PeopleSerializer(ModelSerializer):
    class Meta:
        model = People
        fields = [
            'id',
            'first_name',
            'last_name',
        ]
