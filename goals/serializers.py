from rest_framework import serializers
from core.serializers import ProfileSerializer
from goals.mixins import ValidationMixin
from goals.models import Comment, GoalCategory, Goal


class CategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CategoryCreateSerializer(CategorySerializer, ValidationMixin):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class GoalSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(GoalSerializer, ValidationMixin):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentCreateSerializer(CommentSerializer, ValidationMixin):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
