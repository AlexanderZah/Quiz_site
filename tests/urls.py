from django.urls import path
from .views import (
    HomeView, SignupUser, logout_user, CategoriesTestsView, TestsView, TestView, ResultView,
    LoginUser
)


urlpatterns = [
    ### Home page ###
    path('', HomeView.as_view(), name='home'),
    ### ###

    ### AUTH ###
    path('signup/', SignupUser.as_view(), name='signup_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    ### ###
    path('category/<int:cat_id>', CategoriesTestsView.as_view(), name='category'),
    path('tests/', TestsView.as_view(), name='tests'),
    path('test/<int:test_id>', TestView.as_view(), name='test'),
    path('result/<int:test_id>', ResultView.as_view(), name='result'),
    
]
