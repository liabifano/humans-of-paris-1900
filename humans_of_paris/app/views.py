from django.shortcuts import render
from app.models import Project


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
    return render(request, 'people.html')


def person(request, id):
    context = {'id': id}
    return render(request, 'person.html', context)


def search(request):
    return render(request, 'search.html')


def upload(request):
    return render(request, 'upload.html')
