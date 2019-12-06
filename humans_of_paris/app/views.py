import os
from django.shortcuts import render
from app.models import Gallica, Tags
from django.core.paginator import Paginator

from PIL import Image
from humans_of_paris.settings import STATICFILES_DIRS



def people(request):
    return

    # return render(request, 'people.html', context={'data': data})


def record(request, id):
    record_data = Gallica.objects.all().get(id=id)
    context = {'record': record_data}
    import pdb; pdb.set_trace()
    return render(request, 'record.html', context)


def person_records(request, name):
    return
    # data = AllData.objects.all().filter(name=name).values('id', 'gallica_image_url', 'date')
    # return render(request, 'person_records.html', context={'data': data})


def home(request):
    tags =[x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]

    if request.method=='POST':
        tag = request.POST.get('myTag')
        ids = Paginator(Tags.objects.filter(tag=tag), 9)
    else:
        ids = Paginator(Gallica.objects.order_by('id'), 9)

    page = request.GET.get('page')
    ids = ids.get_page(page)

    context = {'tags': tags, 'ids': ids}

    return render(request, 'main.html', context)


def cluster(request):
    tags = [x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    context = {'tags': tags}

    return render(request, 'tnse.html', context)


def yourdoppelganger(request):
    if request.method == 'GET':
        context = None
        return render(request, 'upload.html', context)

    else:
        # image = Image.open(request.FILES['image'])
        # image_path = os.path.join(STATICFILES_DIRS[0], 'yourphoto.jpg')
        # image.save(image_path, 'jpg')
        # get file
        ### need most famous
        # make post to http://localhost:5000
        # get most close ids
        context = {'ids': ['btv1b530503232', 'btv1b530503232', 'btv1b530503232',
                           'btv1b530503232', 'btv1b530503232', 'btv1b530503232']}
        # context['your_image'] = image_path
        return render(request, 'doppelganger.html', context)

