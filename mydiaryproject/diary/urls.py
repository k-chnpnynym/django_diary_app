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
]