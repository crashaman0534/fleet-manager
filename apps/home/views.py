from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from apps.home.models import DeviceModel, TopicModel


# Create your views here.
@login_required(login_url="/login/")
def index(request):
    context = {'devicelist': DeviceModel.objects.all(), 'topiclist': TopicModel.objects.all()}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def new_device(request):
    if request.method == 'POST':
        vin = request.POST['vin']
        ip = request.POST['ip']
        port = request.POST['port']

        if DeviceModel.objects.filter(vin=vin).exists():
            return redirect('/new_device')
        else:
            DeviceModel.objects.create(vin=vin, ip=ip, port=port)
            return redirect('/new_device')

    context = {'devicelist': DeviceModel.objects.all(), 'topiclist': TopicModel.objects.all()}
    html_template = loader.get_template('home/new_device.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def new_topic(request):
    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']

        if TopicModel.objects.filter(name=name).exists():
            return redirect('/new_topic')
        else:
            if type == '0':	# publish
                TopicModel.objects.create(name=name, isPub=True, isSub=False)
            else:	# subscribe
                TopicModel.objects.create(name=name, isPub=False, isSub=True)
            return redirect('/new_topic')

    context = {'devicelist': DeviceModel.objects.all(), 'topiclist': TopicModel.objects.all()}
    html_template = loader.get_template('home/new_topic.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def remove_device(request, pk):
    device = DeviceModel.objects.get(vin=pk)

    device.delete()
    return redirect('/index')

@login_required(login_url="/login/")
def remove_topic(request, pk):
    topic = TopicModel.objects.get(name=pk)

    topic.delete()
    return redirect('/index')

@login_required(login_url="/login/")
def device(request, pk):
    context = {'devicelist': DeviceModel.objects.all(), 'device': DeviceModel.objects.get(vin=pk),
               'topiclist': TopicModel.objects.all()}

    html_template = loader.get_template('home/device.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def topic(request, pk):
    context = {'devicelist': DeviceModel.objects.all(), 'topiclist': TopicModel.objects.all(),
               'topic': TopicModel.objects.get(name=pk)}

    html_template = loader.get_template('home/topic.html')
    return HttpResponse(html_template.render(context, request))
