from django.urls import path
from . import views

urlpatterns = [
    path("start/<int:topic_id>/", views.start_test, name="start_test"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("topics/", views.topic_list, name="topic_list"),
    path("company-tests/", views.company_test_list, name="company_test_list"),
path("company-start/<int:company_id>/", views.company_start_test, name="company_start_test"),

]