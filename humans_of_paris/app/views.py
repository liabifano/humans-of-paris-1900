from django.shortcuts import render
from app.models import AllData, UploadImage
from django.db.models import Max, Count
from django.http import HttpResponse, HttpResponseForbidden


def people(request):
    data = (AllData.objects.all()
            .filter(wiki_url__isnull=False)
            .order_by('-wiki_n_images')
            .values('name',
                    'wiki_url',
                    'wiki_url',
                    'wiki_n_images',
                    'wiki_n_references'
                    )
            .annotate(Count('id'),
                      Max('gallica_image_url'),
                      Max('tag_sex'),
                      Max('tag_profession'))
            .distinct())[:20]

    return render(request, 'people.html', context={'data': data})


def record(request, id):
    data = AllData.objects.all().get(id=id)

    return render(request, 'record.html', context={'data': data})


def person_records(request, name):
    data = AllData.objects.all().filter(name=name).values('id', 'gallica_image_url', 'date')
    return render(request, 'person_records.html', context={'data': data})


def search(request):
    context = {'tags':
                   ['female', 'male', 'artist', 'actor', 'photographer']}
    return render(request, 'search.html', context)


def home(request):
    context = None
    return render(request, 'main.html', context)


def cluster(request):
    context=None
    return render(request, 'tnse.html', context)

def yourdoppelganger(request):
    context=None
    return render(request, 'doppelganger.html', context)

def upload(request):
    if request.method == 'POST':
        form = UploadImage(request.POST, request.FILES)
        import pdb; pdb.set_trace()
        form.save()
        return HttpResponse('image upload success')
    else:
        context = None
        return render(request, 'upload.html', context)
