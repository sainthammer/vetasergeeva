from django.urls import path
from .views import (
    index_view,
    about_view,
    contacts_view,
    portfolio_view,
    services_view,
    project_detail_view,
)

app_name = "landing"

urlpatterns = [
    path("", index_view, name="index_view"),
    path("about/", about_view, name="about_view"),
    path("contacts/", contacts_view, name="contacts_view"),
    path("portfolio/", portfolio_view, name="portfolio_view"),
    path("portfolio/<slug:slug>/", project_detail_view, name="project_detail"),
    path("services/", services_view, name="services_view"),
]
