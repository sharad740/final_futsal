from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from . import models

class SuccessMessageMixin:
    success_message = ""
    failure_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_success_message(form)
        return response

    def form_invalid(self,form):
        response = super().form_invalid(form)
        self.send_failure_message(form)
        return response
    
    def send_success_message(self,form):
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

    def send_failure_message(self,form):
        failure_message = self.get_failure_message(form.cleaned_data)
        if failure_message:
            messages.error(self.request, failure_message)


    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_failure_message(self, cleaned_data):
        return self.failure_message % cleaned_data

class IsAdminOnlyMixin(LoginRequiredMixin,UserPassesTestMixin):
    permission_denied_message = "No permission granted to access this page."

    def test_func(self):
        return self.request.user.is_staff

class IsOwnerOnlySingleObjectMixin(LoginRequiredMixin,UserPassesTestMixin):
    user_field = 'user'
    permission_denied_message = "You are not authorized to access this page"

    def get_user_field(self):
        return self.user_field

    def test_func(self):
        model_attr = self.get_user_field()
        current_user = self.request.user
        return current_user == getattr(self.get_object(), model_attr)

class GetPostMixin:
    post_context_object_name = "post"
    
    def get_post(self):
        pk_post = self.kwargs.get("pk")
        if not hasattr(self,"post_obj"):
            self.post_obj = get_object_or_404(models.Post,id=pk_post)
        return self.post_obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.post_context_object_name] = self.get_post()
        return context

class IsCordinatorMixin(LoginRequiredMixin,UserPassesTestMixin,GetPostMixin):
    def test_func(self):
        post = self.get_post()
        return post.get_cordinator_user() == self.request.user 
    
class IsGameManagerMixin(LoginRequiredMixin,UserPassesTestMixin,GetPostMixin):
    def test_func(self):
        post = self.get_post()
        return post.get_gm_user() == self.request.user 
    
