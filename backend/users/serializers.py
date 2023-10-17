from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import (UniqueTogetherValidator,
                                       UniqueValidator,
                                       ValidationError)

from api.commomserializers import ShortRecipeSerializer
from cookingcrafts.constants import User as U

from .models import Subscribe, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\z",
        max_length=U.MAX_USERNAME,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=U.MAX_EMAIL_FIELD,
        validators=[UniqueValidator(queryset=User.objects.all)]
    )

    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (not user.is_anonymous
                and obj.subscribing.filter(user=user).exists())


class SubscribeListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('__all__',)

    def get_is_subscribed(self, obj):
        user = self.context.get('user')
        return (not user.is_anonymous
                and obj.subscribing.filter(user=user).exists())

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        author_recipes = obj.recipes.all()
        if limit:
            author_recipes = author_recipes[:int(limit)]
        return ShortRecipeSerializer(author_recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('author', 'user')
        model = Subscribe
        validators = [UniqueTogetherValidator(
            queryset=Subscribe.objects.all(),
            fields=('user', 'author'),
            message='Subscription already exists!')]

    def validate(self, data):
        if data.get('user').id == data.get('author').id:
            raise ValidationError(
                'You cannot subscribe to yourself!'
            )
        return data

    def create(self, validated_data):
        author = validated_data.get('author')
        user = validated_data.get('user')
        return Subscribe.objects.create(user=user, author=author)

    def to_representation(self, instance):
        context = {'request': self.context.get('request'),
                   'user': instance.user}
        return SubscribeListSerializer(instance=instance.author,
                                       context=context).data
