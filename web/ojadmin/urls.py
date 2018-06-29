from .views import *
from django.urls import path

urlpatterns = [
    path('', admin, name='admin'),
    path('add_problem/', add_problem, name='add_problem'),
    path('add_contest/',add_contest, name='add_contest'),
    path('problem_list/', problem_list, name='problem_list'),
    path('problem_add/', problem_add_example, name='problem_add_example'),
    path('problem_add/<id>', problem_add_example, name='problem_add_example'),
    path('contest_list/', contest_list, name='contest_list'),
]