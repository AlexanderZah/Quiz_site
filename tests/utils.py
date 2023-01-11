from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = CategoryTest.objects.all()
        tests = Tests.objects.all()
        context['categories'] = cats
        context['tests'] = tests
        return context

class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
