from .models import *


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = CategoryTest.objects.all()
        tests = Tests.objects.all()
        context['categories'] = cats
        context['tests'] = tests
        return context