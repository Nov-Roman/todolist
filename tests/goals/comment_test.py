import pytest
from django.utils import timezone

from goals.serializers import CommentSerializer
from tests.factories import GoalCommentFactory

from goals.models import Comment


@pytest.mark.django_db
def test_comment_create(client, get_credentials, goal):
    """create comment test"""
    data = {
        "text": "testcomm",
        "goal": goal.id,
    }

    response = client.post(
        path="/goals/goal_comment/create",
        data=data,
        content_type="application/json",
        HTTP_AUTHORIZATION=get_credentials,
    )
    comment = Comment.objects.last()
    assert response.status_code == 201
    assert response.data == {
        "id": comment.id,
        "created": timezone.localtime(comment.created).isoformat(),
        "updated": timezone.localtime(comment.updated).isoformat(),
        "text": "testcomm",
        "goal": goal.id
    }


@pytest.mark.django_db
def test_comment_list(client, get_credentials, goal, board_participant):
    """comment list test"""
    comments = GoalCommentFactory.create_batch(5, user=goal.user, goal=goal)
    comments.sort(key=lambda x: x.id, reverse=True)

    response = client.get(
        path="/goals/goal_comment/list",
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == CommentSerializer(comments, many=True).data


@pytest.mark.django_db
def test_comment_retrieve(client, get_credentials, comment, board_participant):
    """comment detail test"""
    response = client.get(
        path=f"/goals/goal_comment/{comment.id}",
        HTTP_AUTHORIZATION=get_credentials
    )

    assert response.status_code == 200
    assert response.data == CommentSerializer(comment).data


@pytest.mark.django_db
def test_comment_update(client, get_credentials, comment, board_participant):
    """comment update test"""
    new_text = "updated_text"

    response = client.patch(
        path=f"/goals/goal_comment/{comment.id}",
        HTTP_AUTHORIZATION=get_credentials,
        data={"text": new_text},
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.data["text"] == new_text


@pytest.mark.django_db
def test_comment_delete(client, get_credentials, comment, board_participant):
    """comment delete test"""
    response = client.delete(
        path=f"/goals/goal_comment/{comment.id}",
        HTTP_AUTHORIZATION=get_credentials,
    )

    assert response.status_code == 204
    assert response.data is None
