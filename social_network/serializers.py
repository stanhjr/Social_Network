from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import MyUser, Post
from .tools import is_fan, get_count_like


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['username', 'password']

    def save(self, **kwargs):
        self.validated_data["password"] = make_password(self.validated_data["password"])
        return super().save()


class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'count_like', 'is_fan', 'author']

    def get_is_fan(self, obj) -> bool:
        """
        checking if the user has licked this post
        """
        user = self.context.get('request').user
        return is_fan(obj, user)

    def get_count_like(self, obj) -> int:
        return get_count_like(obj)

    def get_author(self, obj):
        user = obj.author
        return {'id': user.id, 'username': user.username}

    def validate(self, data):
        data['author_id'] = self.context['request'].user.id
        return data


class FanSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = (
            'user_id',
            'username',
        )

    def get_user_id(self, obj):
        return obj.id


class DateSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['date_from'] > data['date_to']:
            raise serializers.ValidationError("finish must occur after start")
        return data





