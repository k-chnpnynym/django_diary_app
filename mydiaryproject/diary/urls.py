from django.urls import path

from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('diary_create/', views.DiaryCreateView.as_view(), name='diary_create'),
    path('diary_create_complete/', views.DiaryCreateCompleteView.as_view(), name='diary_create_complete'),
    path('diary_list/', views.DiaryListView.as_view(), name='diary_list'),  # 追記
    path('diary_detail/<uuid:pk>/', views.DiaryDetailView.as_view(), name='diary_detail'),  # 追記
    path('diary_update/<uuid:pk>/', views.DiaryUpdateView.as_view(), name='diary_update'),  # 追記
    path('diary_delete/<uuid:pk>/', views.DiaryDeleteView.as_view(), name='diary_delete'),  # 追加
    path('tag/<slug:tag>/', views.DiaryTagView.as_view(), name='diary_tag_list'),
    path('tag/config/list/', views.TagListView.as_view(), name='tag_list'),
    path('tag/config/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag/config/update/<int:pk>/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tag/config/delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view() , name='comment_delete'),
    path('comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='comment_edit'),
]