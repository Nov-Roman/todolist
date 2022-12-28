from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import permissions, filters
from goals.filters import GoalDateFilter

from goals.models import Board, Goal, GoalCategory, Comment
from goals.permissions import BoardPermissions, CategoryPermissions, CommentPermissions, GoalPermissions
from goals.serializers import (
    BoardCreateSerializer,
    BoardListSerializer,
    BoardSerializer,
    CategoryCreateSerializer,
    CategorySerializer,
    CommentCreateSerializer,
    CommentSerializer,
    GoalCreateSerializer,
    GoalSerializer,
)
from rest_framework.pagination import LimitOffsetPagination


class BoardCreateView(CreateAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    pagination_class = LimitOffsetPagination
    serializer_class = BoardListSerializer
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=("is_deleted",))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived)
        return instance


class CategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [CategoryPermissions]
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class CategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=("is_deleted",))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["priority", "due_date"]
    ordering = ["priority", "due_date"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [CommentPermissions]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering = ["-id"]

    def get_queryset(self):
        return Comment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user=self.request.user)
