from django.urls import path

from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("scraping_status/<str:id>/", views.get_status, name="get_status")
]
