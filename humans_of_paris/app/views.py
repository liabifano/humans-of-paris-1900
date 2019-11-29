from django.shortcuts import render
from app.models import Gallica, Tags
from django.db.models import Max, Count
from django.http import HttpResponse, HttpResponseForbidden


def people(request):
    return

    # return render(request, 'people.html', context={'data': data})


def record(request, id):
    return


def person_records(request, name):
    return
    # data = AllData.objects.all().filter(name=name).values('id', 'gallica_image_url', 'date')
    # return render(request, 'person_records.html', context={'data': data})


def home(request):
    tags =[x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]

    if request.method=='POST':
        tag = request.POST.get('myTag')
        ids = [i.gallica.id for i in Tags.objects.filter(tag=tag).iterator()][0:8]
    else:
        records = [{'gallica': i,
                    'tags': ' '.join([x.tag for x in i.tags_set.iterator()])}
                   for i in list(Gallica.objects.order_by('id').iterator())[100:130]]

    context = {'tags': tags, 'records': records}

    return render(request, 'main.html', context)


def cluster(request):
    tags = [x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    context = {'tags': tags}

    return render(request, 'tnse.html', context)


def yourdoppelganger(request):
    tags =[x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    context = {'tags': tags}

    return render(request, 'doppelganger.html', context)

