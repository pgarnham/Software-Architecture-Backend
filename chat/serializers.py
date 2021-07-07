from rest_framework_json_api import serializers
from chat.models import Message, User, Room

class MessageSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(slug_field="name",read_only=True)
    class Meta:
        model = Message
        fields = ('id','author', 'content','room', 'timestamp')
        read_only_fields = ('id','timestamps')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'username','is_admin')
        read_only_fields = ('id',)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id','name', 'is_private','author','accepted_users')
        read_only_fields = ('id',)
