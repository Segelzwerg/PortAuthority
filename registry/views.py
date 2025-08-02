from django.shortcuts import render
from django.views.generic import ListView

from .models import Application


class ApplicationListView(ListView):
    """
    View to display all applications in the database.

    This view provides a paginated list of all Application instances
    with their protocol, URL, port, and full address.
    """

    model = Application
    template_name = "registry/application_list.html"
    context_object_name = "applications"
    paginate_by = 20  # Show 20 applications per page
    ordering = ["protocol", "url", "port"]  # Order by protocol, then URL, then port

    def get_context_data(self, **kwargs):
        """Add additional context data to the template."""
        context = super().get_context_data(**kwargs)
        context["total_applications"] = Application.objects.count()
        return context


def application_list(request):
    """
    Function-based view alternative to display all applications.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponse: Rendered template with applications list
    """
    applications = Application.objects.all().order_by("protocol", "url", "port")
    context = {
        "applications": applications,
        "total_applications": applications.count(),
    }
    return render(request, "registry/application_list.html", context)
