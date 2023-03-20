from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class Diary(models.Model):
    app_label = "diary"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name='日付', default=timezone.now)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    text = models.TextField(verbose_name='本文', max_length=200, blank=True)
    image = models.ImageField(upload_to='media/images/', verbose_name='写真', blank=True, null=True)
    secret = models.BooleanField(verbose_name='内緒', default=True)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='編集日時', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return f"{self.title} - {self.date}"