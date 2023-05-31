from django.contrib import admin
from .models import Diary, Tag, Comment

admin.site.register(Diary)
admin.site.register(Tag)
admin.site.register(Comment)

