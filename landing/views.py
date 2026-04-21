from django.shortcuts import render, get_object_or_404, redirect
from .models import AboutPage, Project, ContactsPage, HomePage, ServicesPage
from .forms import ContactRequestForm


def index_view(request):
    page = HomePage.objects.prefetch_related(
        "stats",
        "services",
        "approach_steps",
    ).first()

    return render(
        request,
        "landing/home.html",
        {
            "page": page,
        },
    )


def about_view(request):

    page = AboutPage.objects.prefetch_related("values", "timeline_items").first()

    context = {
        "page": page,
    }

    return render(request, "landing/about.html", context)


def contacts_view(request):
    page = ContactsPage.objects.first()

    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{request.path}?success=1")
    else:
        form = ContactRequestForm()

    return render(
        request,
        "landing/contacts.html",
        {
            "page": page,
            "form": form,
            "success": request.GET.get("success") == "1",
        },
    )


def services_view(request):
    page = ServicesPage.objects.prefetch_related("services__features").first()

    return render(
        request,
        "landing/services.html",
        {
            "page": page,
        },
    )


def portfolio_view(request):
    projects = Project.objects.filter(is_featured=True).prefetch_related("images")
    return render(request, "landing/portfolio.html", {"projects": projects})


def project_detail_view(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related("images"),
        slug=slug,
        is_featured=True,
    )
    return render(request, "landing/project_detail.html", {"project": project})
