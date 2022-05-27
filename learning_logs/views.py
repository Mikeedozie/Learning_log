from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
# Create your views here.


def index(request):
    topics = Topic.objects.all()
    context = {'topics':topics}
    return render(request, 'index.html', context)

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

@login_required
def entries(request, topic_id):
    topics = Topic.objects.get(id=topic_id)
    if topics.owner != request.user:
        return Http404
    entries = topics.entry_set.order_by('-date_added')
    context = {'topics': topics, 'entries': entries}
    return render(request, 'entry.html', context)



@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            own = form.save(commit=False)
            own.owner = request.user
            own.save()
            return HttpResponseRedirect(reverse('topics'))
    context ={'form': form}
    return render(request, 'new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topics = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.topic = topics
            new_form.save()
            return HttpResponseRedirect(reverse('entries', args=[topic_id]))
        
    context ={'topics': topics, 'form': form}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    user_topics = Topic.objects.all()
    entries = Entry.objects.get(id=entry_id)
    topic = entries.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entries)
    else:
        form = EntryForm(request.POST, instance=entries)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('entries', args=[topic.id]))
    context = {'entries': entries, 'form': form, 'topic': topic, 'user_topics': user_topics}
    return render(request, 'edit_entry.html', context)

@login_required
def delete_entry(request, entry_id, topic_id):
    entry_name = Entry.objects.get(id=entry_id)
    topic = entry_name.topic
    if request.user != topic.owner:
        return Http404
    entry = Entry.objects.get(id=entry_id).delete()
    
    return HttpResponseRedirect(reverse('entries', args=[topic_id]))


def page_not_found_view(request, exception):
    return render(request, '404.html')
    


def view_500(request, exception=None):
    return render(request, '500.html')


def csrf_view(request, exception=None):
    return render(request, '403_csrf.html')