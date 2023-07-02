import os
import uuid

import cv2
from django.conf import settings
from django.db import models
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils import timezone
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


class Tag(models.Model):
    """
    Diary につけられるタグ。

    ひとつの Diary に複数つけられる。
    また、同じタグを複数の Diary につけることができる。

    unique=True のものフィールドの値は、同一モデル内で重複できない
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('diary:diary_tag_list', args=[self.slug])


class Diary(models.Model):
    app_label = "diary"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name='日付', default=timezone.now)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    text = models.TextField(verbose_name='本文', max_length=2000, blank=True, null=True)
    image = models.ImageField(upload_to='images/', verbose_name='写真', blank=True, null=True)
    image_video = models.ImageField(upload_to='video_images/', verbose_name='動画のサムネイル', blank=True, null=True)
    video = models.FileField(upload_to='videos/', verbose_name='動画', blank=True, null=True)  # 動画用のフィールドを追加

    secret = models.BooleanField(verbose_name='内緒', default=True)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    updated_at = models.DateTimeField(verbose_name='編集日時', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(200, 200)], format='JPEG',options={'quality': 60}, )
    thumbnail_video = ImageSpecField(source='image_video', processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 60}, )
    thumbnail_video_detail = ImageSpecField(source='image_video', processors=[ResizeToFill(400, 400)], format='JPEG', options={'quality': 60}, )


    def __str__(self):
        return f"{self.title} - {self.date}"


    def get_absolute_url(self):
        return resolve_url('diary:diary_detail', pk=self.pk)




    def save(self, *args, **kwargs):
        output_folder = os.path.join(settings.MEDIA_ROOT, 'video_images/')
        os.makedirs(output_folder, exist_ok=True)  # フォルダを作成する
        if not self.image and not self.image_video:  # image_video の投稿がない場合のみ実行
            super().save(*args, **kwargs)
            if self.video:
                path = self.video.path  # ファイルの保存された場所
                file_name = os.path.basename(path)  # ファイル名部分

                # opencvで1秒地点を読み込む
                cap = cv2.VideoCapture(path)
                cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
                is_success, image = cap.read()

                # 読み込んだ部分を書き出す
                output_path = os.path.join(output_folder, f'{file_name}.jpg')
                cv2.imwrite(output_path, image)

                # 書き出したファイルのパスを、image_videoに格納して保存
                self.image_video.name = f'video_images/{file_name}.jpg'
                self.thumbnail_video.name = f'video_images/{file_name}_thumbnail.jpg'
                self.thumbnail_video_detail.name = f'video_images/{file_name}_detail.jpg'
        super().save(*args, **kwargs)

 
     



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    text = models.TextField(verbose_name='コメント', max_length=500, blank=True)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return resolve_url('diary:diary_detail', pk=self.diary.pk)


