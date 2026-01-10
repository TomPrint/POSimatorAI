from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.shortcuts import redirect, get_object_or_404
from django.views import View

from .models import User
from .forms import UserCreateForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # dostęp dla admina (is_staff) lub superusera
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('login')
class UserLoginView(LoginView):
    template_name = "users/login.html"

class UserLogoutView(LogoutView):
    pass


class DashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()  # lista wszystkich użytkowników
        return context

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/create_user.html"
    success_url = reverse_lazy("dashboard")


class BlockUserView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        # Nie pozwalamy adminowi zablokować siebie
        if user != request.user:
            user.is_active = not user.is_active  # zmiana statusu aktywności
            user.save()
        return redirect('dashboard')

class DeleteUserView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        # Nie pozwalamy adminowi usunąć siebie
        if user != request.user:
            user.delete()
        return redirect('dashboard')