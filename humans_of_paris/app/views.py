import os
import subprocess
import ast
from django.shortcuts import render
from app.models import Gallica, Tags, Person, Wiki
from django.core.paginator import Paginator

from PIL import Image
from humans_of_paris.settings import STATICFILES_DIRS
from app.get_doppelganger import get_doppelganger




def person(request, name):
    ALL_TAGS = [x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    context = {'tags': ALL_TAGS}
    context['person'] = Person.objects.all().get(name=name)
    context['person_tags'] = Person.objects.all().get(name=name).tags_set.values()
    context['gallicas'] = Person.objects.all().get(name=name).gallica_set.values()
    return render(request, 'person.html', context)


def home(request):
    ALL_TAGS = [x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    DEFAULT_ORDER = 'n_images_wiki'

    if request.method=='POST':
        if request.POST.get('myTag'):
            tag = request.POST.get('myTag')
            ids = Paginator([x.person
                             for x in Tags.objects.all().filter(tag=tag).iterator()], 9)

        elif request.POST.get('order'):
            new_order = request.POST.get('order')
            ids = Paginator(Person.objects.all().order_by('-' + new_order), 9)

        else:
            ids = Paginator(Person.objects.all().order_by('-' + DEFAULT_ORDER), 9)

    else:
        ids = Paginator(Person.objects.all().order_by('-' + DEFAULT_ORDER), 9)

    page = request.GET.get('page')
    ids = ids.get_page(page)

    context = {'persons': ids, 'tags': ALL_TAGS}

    return render(request, 'main.html', context)


def cluster(request):
    ALL_TAGS = [x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    context = {'tags': ALL_TAGS}

    return render(request, 'tnse.html', context)


def yourdoppelganger(request):
    ALL_TAGS = [x[0] for x in Tags.objects.order_by().values_list('tag').distinct().iterator()]
    if request.method == 'GET':
        context = {'tags': ALL_TAGS}
        return render(request, 'upload.html', context)

    else:
        image = Image.open(request.FILES['image'])
        image_path = os.path.join(STATICFILES_DIRS[0], 'tmp/yourphoto.png')
        image.save(image_path)
        cmd = ['curl', '-X', 'POST', '-F', 'image=@{}'.format(image_path), 'http://localhost:5000/get_vector']
        your_vector = str(subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]).split('\\n')[3]
        your_vector = ast.literal_eval((ast.literal_eval(your_vector[:-1])['vector']))

        closests = get_doppelganger(your_vector)
        closest_persons = []

        for id, distance in closests:
            closest_persons.append(
                {'person': Gallica.objects.all().get(gallica_id=id).person,
                 'distance': distance})

        context = {'persons': closest_persons,
                   'your_image': image_path.split('/')[-1]}

        return render(request, 'doppelganger.html', context)

