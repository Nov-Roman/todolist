from django.core.management.base import BaseCommand
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory, BoardParticipant
from ToDoList.settings import BOT_TOKEN


class Command(BaseCommand):
    help = 'Запуск и функционал телеграм-бота'
    tg_client = TgClient(BOT_TOKEN)
    offset = 0

    def get_goals(self, msg: Message, tg_user: TgUser):
        """ Получение и вывод ботом всех целей юзера """

        goals = Goal.objects.filter(category__board__participants__user=tg_user.user).exclude(
            status=Goal.Status.archived)
        goals_str = '\n'.join(['- ' + goal.title for goal in goals])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Вот список твоих целей:\n{goals_str}'
        )

    def create_goal(self, msg: Message, category: GoalCategory, tg_user: TgUser):
        """ Создание юзером цели в ранее выбранной им категории"""

        self.tg_client.send_message(chat_id=msg.chat.id, text='Напиши название для своей новой цели')
        # получаем в ответ название новой цели:
        flag = True
        while flag:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1

                if item.message.text == 'cancel':
                    self.tg_client.send_message(chat_id=msg.chat.id, text='Ты передумал? Ок :)')
                    flag = False
                else:
                    new_goal = Goal.objects.create(title=item.message.text, category=category, user=tg_user.user)
                    new_goal.save()
                    self.tg_client.send_message(chat_id=msg.chat.id, text='Новая цель создана')
                    flag = False

    def choose_category(self, msg: Message, tg_user: TgUser):
        """ Выбор юзером категории при создании новой цели """

        # предлагаем юзеру выбрать для создаваемой цели категорию  из имеющихся:
        categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            board__participants__role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
            is_deleted=False
        )
        if not categories:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text='У тебя нет ни одной категории. Можешь создать первую в своем аккаунте на сайте mytodolist.tk'
            )

        categories_str = '\n'.join(['- ' + category.title for category in categories])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Выбери категорию для цели из списка:\n{categories_str}'
        )

        # получаем в ответ название категории:
        flag = True
        while flag:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1

                if item.message.text in categories_str:
                    category = categories.filter(title=item.message.text).first()
                    self.create_goal(msg, category, tg_user)
                    flag = False
                elif item.message.text == 'cancel':
                    self.tg_client.send_message(chat_id=msg.chat.id, text='Ты передумал? Ок :)')
                    flag = False
                else:
                    self.tg_client.send_message(chat_id=msg.chat.id,
                                                text='Такой категории нет. Попробуй еще раз или введи cancel если передумал')

    def handle_user(self, msg: Message):
        """ Проверка наличия пользователя в БД, выдача верификационного кода новому юзеру """

        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.from_.id,
            tg_chat_id=msg.chat.id)

        if created:
            self.tg_client.send_message(chat_id=msg.chat.id, text='Привет!')
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Подтверди, пожалуйста, свой аккаунт. '
                     f'Для подтверждения необходимо ввести код: {tg_user.verification_code} на сайте!')
            tg_user.save()
        return tg_user

    def handle(self, *args, **options):
        """ Запуск бота """

        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1

                if hasattr(item, 'message'):
                    tg_user = self.handle_user(item.message)

                    if item.message.text == '/goals':
                        self.get_goals(item.message, tg_user)

                    elif item.message.text == '/create':
                        self.choose_category(msg=item.message, tg_user=tg_user)

                    elif item.message.text == 'cancel':
                        self.tg_client.send_message(chat_id=item.message.chat.id, text='Ты передумал? Ок :)')

                    else:
                        self.tg_client.send_message(chat_id=item.message.chat.id, text='Неизвестная команда')
