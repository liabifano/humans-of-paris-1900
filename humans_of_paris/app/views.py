from django.shortcuts import render
from app.models import AllData


# def project_index(request):
#     projects = Project.objects.all()
#     context = {
#         'projects': projects
#     }
#     return render(request, 'project_index.html', context)
#
#
# def project_detail(request, pk):
#     project = Project.objects.get(pk=pk)
#     context = {
#         'project': project
#     }
#     return render(request, 'project_detail.html', context)


def people(request):
    context = None
    return render(request, 'people.html', context)


def person(request, id):
    context = {'id': id}
    return render(request, 'person.html', context)


def search(request):
    context = None
    return render(request, 'search.html', context)


def upload(request):
    context = None
    return render(request, 'upload.html', context)
