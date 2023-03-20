from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import DiaryForm, DiaryStaffForm
from .models import Diary


class IndexView(TemplateView):
    template_name = 'index.html'


class DiaryCreateView(CreateView):
    template_name = 'diary_create.html'
    form_class = DiaryForm
    success_url = reverse_lazy('diary:diary_create_complete' )

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

class DiaryCreateCompleteView(TemplateView):
    template_name = 'diary_create_complete.html'


class DiaryListView(LoginRequiredMixin, ListView):
    template_name = 'diary_list.html'
    model = Diary

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if not self.request.user.is_staff:
    #         queryset = queryset.exclude(secret=True)
    #     return queryset

    def get_queryset(self):
        if self.request.user.is_staff:
            return Diary.objects.all()
        else:
            return Diary.objects.filter(secret=False)

class DiaryListView(LoginRequiredMixin, ListView):
    template_name = 'diary_list.html'
    model = Diary
    paginate_by = 2   # 1ページあたりの表示数

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if not self.request.user.is_staff:
    #         queryset = queryset.exclude(secret=True)
    #     return queryset

    def get_queryset(self):
        if self.request.user.is_staff:
            return Diary.objects.all()
        else:
            return Diary.objects.filter(secret=False)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     diaries = self.get_queryset()
    #     paginator = Paginator(diaries, self.paginate_by)
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     context['page_obj'] = page_obj
    #     return context

class DiaryDetailView(DetailView):
    template_name = 'diary_detail.html'
    model = Diary


class DiaryUpdateView(UpdateView):
    template_name = 'diary_update.html'
    model = Diary
    fields = ('date', 'title', 'text', 'image')
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


class DiaryDeleteView(DeleteView):
    template_name = 'diary_delete.html'
    model = Diary
    success_url = reverse_lazy('diary:diary_list')