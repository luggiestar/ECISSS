from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Topic
from ..forms import TopicForm
from django.db.utils import IntegrityError


@login_required(login_url='/')
def topic_list(request):
    get_topic = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():

            get_form = form.save(commit=False)
            get_form.name = request.POST['name'].upper()
            get_form.save()

            messages.success(request, f"Topic created successfully")
            return redirect('topic_list')

        else:
            messages.error(request, f"Topic not created successfully")
            return redirect('topic_list')

    context = {
        'topics': get_topic,
        'form': TopicForm
    }

    return render(request, 'pages/topics.html', context)


@login_required(login_url='/')
def edit_topic(request, topic_id):
    instance = Topic.objects.filter(id=topic_id).first()
    if request.method == 'POST':
        try:
            form = TopicForm(request.POST, instance=instance)
            if form.is_valid():
                try:
                    get_form = form.save(commit=False)
                    get_form.name = request.POST['name'].upper()
                    get_form.save()
                    messages.success(request, f"Topic edited successfully")
                    return redirect('topic_list')
                except IntegrityError:
                    messages.error(request, f"Topic with the given name all ready exist")
                    return redirect('topic_list')
        except:
            messages.error(request, f"Topic with the given id does not exist")
            return redirect('topic_list')
    context = {
        'form': TopicForm(instance=instance)
    }

    return render(request, 'pages/edit-topic.html', context)


@login_required(login_url='/')
def delete_topic(request):
    if request.method == 'POST':
        topic_id = request.POST['topic_id']
        try:
            get_level = get_object_or_404(Topic, id=topic_id)
            name = f'{get_level.name}'
            get_level.delete()
            messages.success(request, f"{name} deleted successfully")
            return redirect('topic_list')
        except:
            messages.error(request, f"Topic with the given id does not exist")
            return redirect('topic_list')
