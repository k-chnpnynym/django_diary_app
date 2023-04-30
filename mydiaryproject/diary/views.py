from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import DiaryForm, DiaryStaffForm, DiaryCommentForm
from .models import Diary, Tag



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'



class DiaryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'diary_create.html'
    form_class = DiaryForm
    success_url = reverse_lazy('diary:diary_create_complete' )

    def get_queryset(self):
        return Diary.objects.all().select_related('user')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# @login_required
# def diary_create(request):
#     if request.method == 'POST':
#         form = DiaryForm(request.POST, request.FILES)
#         if form.is_valid():
#             diary = form.save(commit=False)
#             diary.save()
#             return redirect('diary:diary_detail', pk=diary.pk)
#     else:
#         form = DiaryForm()
#     return render(request, 'diary_form.html', {'form': form})

class DiaryCreateCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'diary_create_complete.html'


class DiaryListView(LoginRequiredMixin, ListView):
    template_name = 'diary_list.html'
    model = Diary
    paginate_by = 10   # 1ページあたりの表示数


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag')
        context['keyword'] = self.request.GET.get('keyword', '')
        return context



    # def get_queryset(self):
    #     if self.request.user.is_staff:
    #         return Diary.objects.all().select_related('user')
    #     else:
    #         return Diary.objects.filter(secret=False).select_related('user')
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user').prefetch_related('tags').order_by('date')
        selected_tag = self.request.GET.get('tag')
        if selected_tag:
            queryset = queryset.filter(tags__slug=selected_tag)
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword) |
                                       Q(date__icontains=keyword) | Q(user__username__icontains=keyword))

        if not self.request.user.is_staff:
            queryset = queryset.exclude(secret=True)
        return queryset


class DiaryTagListView(DiaryListView):
    model = Diary

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs['tag']).select_related('user').prefetch_related('tags')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag'])
        return context


class DiaryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'diary_detail.html'
    model = Diary
    def get_queryset(self):
        return Diary.objects.all().select_related('user').prefetch_related('tags', 'comment_set', 'comment_set__user',)

    def post(self, request, *args, **kwargs):
        form = DiaryCommentForm(request.POST)
        if form.is_valid():
            self.object = self.get_object()
            comment = form.save(commit=False)
            comment.diary = self.object
            comment.user = self.request.user  # 要ログイン。ログインユーザ以外によるコメントはここで 500 エラーになる
            comment.save()
            messages.info(self.request, 'コメントしました')
            return redirect(self.request.path)
        else:
            messages.info(self.request, 'コメント投稿に失敗しました')
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DiaryCommentForm()
        return context


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'diary_update.html'
    model = Diary
    fields = ('date', 'title', 'text', 'image', 'tags')
    success_url = reverse_lazy('diary:diary_list')

    # def get_form_class(self):
    #     if getattr(self.request.user, settings.STAFF_FLAG_ATTR_NAME, False):
    #         return DiaryStaffForm
    #     return super().get_form_class()

    def get_form_class(self):
        if self.request.user.is_staff:
            return DiaryStaffForm
        return super().get_form_class()

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.updated_at = timezone.now()
        diary.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Diary.objects.all().select_related('user')


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'diary_delete.html'
    model = Diary
    success_url = reverse_lazy('diary:diary_list')

    def get_queryset(self):
        return Diary.objects.all()#.select_related('user')
