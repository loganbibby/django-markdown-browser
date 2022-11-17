from django.urls import path

from .views import MarkdownView


app_name = "docs"


urlpatterns = [
    path(
        "<str:file>",
        MarkdownView.as_view(),
        name="view"
    ),
    path(
        "",
        MarkdownView.as_view(),
        name="index"
    )
]
