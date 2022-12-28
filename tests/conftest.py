from pytest_factoryboy import register

from factories import *

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(GoalCategoryFactory)
register(GoalCommentFactory)
register(GoalFactory)

pytest_plugins = 'tests.fixtures'
