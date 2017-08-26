from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic
from .forms import TopicForm, EntryForm

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


@login_required
def edit_entry(request, entry_id):
  """Edit an existing entry."""
  entry = Entry.objects.get(id=entry_id)
  topic = entry.topic

  if topic.owner != request.user:
    raise Http404

  # 2 Make sure the topic belongs to the current user.
  if topic.owner != request.user:
    raise Http404

  if request.method != 'POST':
    # Initial request;
    #  initialize form with the current entry.
    form = EntryForm(instance=entry)
  else:
    # POST data submitted; process data.
    form = EntryForm(instance=entry, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(
        reverse('learning_logs:topic',
                args=[topic.id]))

  context = {'entry': entry,
             'topic': topic,
             'form': form}
  return render(
    request,
    'learning_logs/edit_entry.html',
    context)


@login_required
def new_entry(request, topic_id):
  """Add a new entry for a particular topic."""
  topic = Topic.objects.get(id=topic_id)

  if request.method != 'POST':
    # No data submitted; create a blank form.
    form = EntryForm()
  else:
    # POST data submitted; process data.

    # gather data from form
    form = EntryForm(data=request.POST)
    if form.is_valid():
      # create new entry object,
      #   not into database yet
      new_entry = form.save(commit=False)
      new_entry.topic = topic
      # save into db with topic value
      new_entry.save()

      # goto topics w/id
      return \
        HttpResponseRedirect(
          reverse('learning_logs:topic',
                  args=[topic_id]))

  # display new entry form
  context = {'topic': topic,
             'form': form}
  return render(
    request,
    'learning_logs/new_entry.html',
    context)


@login_required
def new_topic(request):
  """Add a new topic."""

  # create a blank form
  # OR
  # validate form and submit data

  # if POST, user may want to submit data to server
  if request.method != 'POST':
    # No data submitted; create a blank form.
    form = TopicForm()
  else:
    # POST data submitted;
    # retrieve data from form, test is_valid
    form = TopicForm(request.POST)
    if form.is_valid():
      # form.save()

      # update owner, then save
      new_topic = form.save(commit=False)  # 1
      new_topic.owner = request.user  # 2
      new_topic.save()  # 3

      # sends browser to topics page display
      return HttpResponseRedirect(
        reverse('learning_logs:topics'))

  context = {'form': form}
  return render(
    request,
    'learning_logs/new_topic.html',
    context)


@login_required
def topic(request, topic_id):
  """Show a single topic and all its entries."""
  # topic = Topic.objects.get(id=topic_id)
  topic = get_object_or_404(Topic, id=topic_id)
  entries = topic.entry_set.order_by('-date_added')

  context = {'topic': topic, 'entries': entries}
  return render(
    request,
    'learning_logs/topic.html',
    context)


@login_required
def topics(request):
  # topics for current login
  topics = Topic.objects.filter(
    owner=request.user).order_by('date_added')

  # topics = Topic.objects.order_by('date_added')

  context = {'topics': topics}
  return render(request,
                'learning_logs/topics.html',
                context)


# Create your views here.
def index(request):
  """The home page for Learning Log"""
  return render(request,
                'learning_logs/index.html')
