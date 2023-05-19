from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import DiaryForm, DiaryStaffForm, DiaryCommentForm
from .models import Diary, Tag, Comment


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'



class DiaryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'diary_create.html'
    form_class = DiaryForm
    success_url = reverse_lazy('diary:diary_list' )

    def get_queryset(self):
        return Diary.objects.all().select_related('user')


    def form_valid(self, form):
        # form.instance.user = self.request.user
        diary = form.save(commit=False)
        diary.user = self.request.user
        if not self.request.user.is_staff:
            diary.secret = False
        diary.save()
        messages.success(self.request, '日記を投稿しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記を投稿できませんでした。')
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['staff_form'] = DiaryStaffForm
        return context


class DiaryCreateCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'diary_create_complete.html'



class DiaryListView(LoginRequiredMixin, ListView):
    template_name = 'diary_list.html'
    model = Diary
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        if page_number:
            context['page_number'] = page_number
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag')
        context['keyword'] = self.request.GET.get('keyword', '')
        context['num_diaries'] = self.request.GET.get('num_diaries', '8')
        context['order_by'] = self.request.GET.get('order_by', '-date')
        page_obj = context['page_obj']
        context['paginator_range'] = page_obj.paginator.get_elided_page_range(page_obj.number)
        return context

    def get_paginate_by(self, queryset):
        num_diaries = self.request.GET.get('num_diaries', '8')

        if num_diaries == 'all':
            num_diaries = Diary.objects.all().count()

        return num_diaries

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', '-date')
        queryset = queryset.select_related('user').prefetch_related('tags').order_by(order_by)
        selected_tag = self.request.GET.get('tag')
        if selected_tag:
            queryset = queryset.filter(tags__slug=selected_tag)
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword) |
                                       Q(date__icontains=keyword) | Q(user__username__icontains=keyword)
                                       # | Q(created_at__icontains=keyword) | Q(updated_at__icontains=keyword)
                                       )

        if not self.request.user.is_staff:
            queryset = queryset.exclude(secret=True)
        return queryset


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
            messages.success(self.request, 'コメントしました')
            self.object = self.get_queryset().get(pk=self.object.pk)
            return redirect(self.request.path)
        else:
            messages.error(self.request, 'コメント投稿に失敗しました')
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DiaryCommentForm()
        context['object'] = self.get_object()
        return context


class DiaryTagView(DiaryListView):
    model = Diary
    template_name = 'diary_list_tag.html'
    paginate_by = 8


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag'])
        context['num_diaries'] = self.request.GET.get('num_diaries', '8')
        context['order_by'] = self.request.GET.get('order_by', '-date')
        context['keyword'] = self.request.GET.get('keyword', '')
        return context


    def get_paginate_by(self, queryset):
        num_diaries = self.request.GET.get('num_diaries', 8)

        if num_diaries == 'all':
            num_diaries = Diary.objects.all().count()

        return num_diaries


    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', '-date')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword) |
                                       Q(date__icontains=keyword) | Q(user__username__icontains=keyword)
                                       # | Q(created_at__icontains=keyword) | Q(updated_at__icontains=keyword)
                                       )
        return queryset.filter(tags__slug=self.kwargs['tag']).select_related('user').prefetch_related('tags').order_by(order_by)




class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'diary_update.html'
    model = Diary
    fields = ('date', 'title', 'text', 'image', 'video', 'image_video', 'tags')

    def get_success_url(self):
        diary_pk = self.object.pk
        return reverse('diary:diary_detail', kwargs={'pk': diary_pk})


    def get_form_class(self):
        if self.request.user.is_staff:
            return DiaryStaffForm
        return super().get_form_class()

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.updated_at = timezone.now()
        diary.save()
        messages.success(self.request, '日記を編集しました。')

        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, '日記を編集できませんでした。')
        return super().form_invalid(form)


    def get_queryset(self):
        return Diary.objects.all().select_related('user')



class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Diary
    template_name = 'diary_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # if not request.user == self.object.user:
        #     messages.error(request, '日記を削除できるのは投稿者だけです。')
        #     return redirect('diary:diary_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, '日記を削除しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:diary_list')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # if not request.user.is_staff:
        #     messages.error(request, 'コメントを削除できるのは管理者だけです。')
        #     return redirect('diary:diary_list')
        return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'コメントを削除しました。')
    #     # return super().form_valid(form)
    #     return response

    def form_valid(self, form):
        if self.request.POST.get("confirm_delete"):
            messages.success(self.request, 'コメントを削除しました。')
        return super().form_valid(form)

    def get_success_url(self):
        diary_pk = self.object.diary.pk
        return reverse('diary:diary_detail', kwargs={'pk': diary_pk})



class CommentEditView(LoginRequiredMixin, UpdateView):
    template_name = 'comment_edit.html'
    model = Comment
    fields = ['text']

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if not (self.request.user.is_staff or self.request.user == comment.user):
            raise Http404
        return comment

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.save()
        messages.success(self.request, 'コメントを編集しました')
        return redirect('diary:diary_detail', pk=self.object.diary.pk)


class TagListView(ListView):
    model = Tag
    template_name = 'tag_list.html'
    context_object_name = 'tags'




class TagCreateView(CreateView):
    model = Tag
    template_name = 'tag_create.html'
    fields = ['name', 'slug']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'タグを作成できるのは管理者だけです。')
            return redirect('diary:tag_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'タグを作成しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:tag_list')


class TagUpdateView(UpdateView):
    model = Tag
    template_name = 'tag_update.html'
    fields = ['name', 'slug']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'タグを更新できるのは管理者だけです。')
            return redirect('diary:diary_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'タグを更新しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:tag_list')


class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'tag_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'タグを削除できるのは管理者だけです。')
            return redirect('diary:diary_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'タグを削除しました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary:tag_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list_url'] = resolve_url('diary:tag_list')
        return context
