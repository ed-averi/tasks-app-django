from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# removing the global tasks variable
# tasks = []


class NewTaskForm(forms.Form):
    # get input from user
    task = forms.CharField(label="New Task")
    # add priority to the task
    priority = forms.IntegerField(label="Priority",
                                  min_value=1, max_value=10)

# views go here


def index(request):
    # adding tasks in session
    if "tasks" not in request.session:
        # if the user does'nt have a list of task, then give them an empty list.
        request.session["tasks"] = []
    return render(request, 'tasks/index.html', {
        # pass the list of tasks to this template
        "tasks": request.session["tasks"]
    })

# adding client and server side validation


def add(request):
    # Check if the method is POST
    if request.method == 'POST':
        # Take in the data the user submitted and save it in the form variable
        form = NewTaskForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # this will give me access to the data submitted by the user
            task = form.cleaned_data["task"]
            # Add the task to the list of tasks
            request.session["tasks"] += [task]
            # Once a new task is submitted, redirect the user to the list of tasks
            return HttpResponseRedirect(reverse('index'))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, 'tasks/add.html', {
                'form': form
            })

    return render(request, 'tasks/add.html', {
        # giving the template access to the variable called form
        "form": NewTaskForm()
    })
