from django.core.validators import MinLengthValidator
from django.db import models
from core.models import User
from django.utils.crypto import get_random_string


class TgUser(models.Model):
    tg_chat_id = models.IntegerField(verbose_name='id чата')
    tg_user_id = models.IntegerField(verbose_name='id пользователя Телеграмм')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь API')
    tg_username = models.CharField(max_length=32, validators=[MinLengthValidator(5)],verbose_name='Имя пользователя Телеграмм')
    verification_code = models.CharField(max_length=10, unique=True, verbose_name='Верификационный код')

    def generate_verification_code(self) -> str:
        ver_code = get_random_string(10)
        self.verification_code = ver_code
        self.save()
        return ver_code

