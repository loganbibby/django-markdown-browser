from io import StringIO
from pathlib import Path
from django.views.generic import TemplateView
from django.http import Http404
from django.utils.html import mark_safe
import pycmarkgfm


__all__ = [
    "MarkdownView"
]


DOCS_DIR = Path("/docs")


class MarkdownView(TemplateView):
    template_name = "markdown.html"
    page_title = "Documentation"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.filename = kwargs.get("file")

        if not self.filename:
            self.filename = "README"

        if not self.filename.endswith(".md"):
            self.filename += ".md"

        self.file = DOCS_DIR / self.filename

        if not self.file.is_file():
            self.file = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        with open(self.file, "r") as fh:
            contents = pycmarkgfm.gfm_to_html(
                "\n".join(fh.readlines())
            )

        # Fix /docs references
        contents = contents.replace("docs/", "")

        ctx["contents"] = mark_safe(contents)
        ctx["filename"] = self.filename

        return ctx

    def get(self, request, *args, **kwargs):
        if not self.file:
            raise Http404()

        return super().get(request, *args, **kwargs)
