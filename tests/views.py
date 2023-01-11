from typing import Any, Dict
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .utils import DataMixin, MyLoginRequiredMixin
from .forms import SignupUserForm
from .models import Question, CategoryTest, Tests, ResultTest


class HomeView(DataMixin, ListView):
    model = CategoryTest
    template_name = "tests/home.html"
    context_object_name = 'categories'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))


class CategoriesTestsView(DataMixin, ListView):
    model = CategoryTest
    template_name = 'tests/category_test.html'
    context_object_name = 'category'

    def get_queryset(self):
        return CategoryTest.objects.get(pk=self.kwargs['cat_id'])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))


class TestsView(DataMixin, ListView):
    model = Tests
    template_name = 'tests/tests.html'
    context_object_name = 'tests'
    queryset = model.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))


class TestView(MyLoginRequiredMixin, DataMixin, ListView):
    model = Tests
    template_name = 'tests/test.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['test'] = self.get_queryset()
        context['test_id'] = context['test'].id
        context['questions'] = self.test.question_set.all()
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))

    def get_queryset(self):
        self.test = Tests.objects.get(id=self.kwargs['test_id'])
        return self.test

    def get(self, request, *args, **kwargs):

        return super().get(self, request, *args, **kwargs)


class ResultView(MyLoginRequiredMixin, DataMixin, ListView):
    model = ResultTest
    template_name = 'tests/result.html'
    request_dict = None

    def save_result(self, user, test, count_ans):
        ResultTest.objects.create(user=user, test=test, result=count_ans)

    def get_context_data(self, **kwargs: Any):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['count_ans'] = self.count_ans
        # context['user'] = User.objects.get()
        context['test'] = self.test
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))

    def count_ans(self):
        key_list = list(self.request_dict.keys())
        count_ans = 0
        print(self.request_dict)
        for key in key_list[1:]:
            question = Question.objects.get(id=int(key))
            if str(question.get_right_answer()) == self.request_dict[key]:
                count_ans += 1

        return count_ans

    def post(self, request, *args, **kwargs):
        self.request_dict = request.POST
        self.count_ans = self.count_ans()
        self.test = Tests.objects.get(pk=self.kwargs['test_id'])
        self.save_result(request.user, self.test, self.count_ans)
        return super().get(self, request, *args, **kwargs)


class ResultsUserView(MyLoginRequiredMixin, DataMixin, ListView):
    model = ResultTest
    template_name = 'tests/results_user.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        c_dict = self.get_user_context()
        context['results'] = self.get_queryset()
        return dict(list(context.items()) + list(c_dict.items()))

    def get_queryset(self):
        return ResultTest.objects.filter(user=self.request.user).order_by('-id')


class SignupUser(DataMixin, CreateView):
    template_name = 'tests/signup_user.html'
    form_class = SignupUserForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'tests/login_user.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_dict = self.get_user_context()

        return dict(list(context.items()) + list(c_dict.items()))

    def get_success_url(self) -> str:
        return reverse_lazy('home')


def logout_user(request):

    logout(request)
    return redirect('home')