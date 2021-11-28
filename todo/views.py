from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import TODO
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


@login_required
def create_to_do(request):
    if request.method == "GET":
        return render(request, 'todo/create_to_do.html', {'form': TodoForm()})

    else:
        try:
            form = TodoForm(request.POST)
            new_to_do = form.save(commit=False)
            new_to_do.user = request.user
            new_to_do.save()
            return redirect('current_to_do')
        except ValueError:
            return render(request, 'todo/create_to_do.html', {'form': TodoForm(), 'error': 'bad data pass in'})


def login_user(request):
    if request.method == "GET":
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html',
                          {'form': AuthenticationForm(), 'error': 'username or password did not match'})
        else:
            login(request, user)
            return redirect('current_to_do')


def signup_user(request):
    if request.method == "GET":
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_to_do')
            except IntegrityError:
                return render(request, 'todo/signup_user.html',
                              {'form': UserCreationForm(), 'error': 'that username is taken , choose a new username'})

        else:
            return render(request, 'todo/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'password did not match'})


@login_required
def current_to_do(request):
    todolist = TODO.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/current_to_do.html', {'todolist': todolist})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def view_to_do(request, todo_pk):
    view_to_do = get_object_or_404(TODO, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=view_to_do)
        return render(request, 'todo/view_to_do.html', {'view_to_do': view_to_do, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=view_to_do)
            form.save()
            return redirect('current_to_do')
        except ValueError:
            return render(request, 'todo/view_to_do.html',
                          {'view_to_do': view_to_do, 'form': form, 'error': 'bad info'})


@login_required
def complete_to_do(request, todo_pk):
    complete_to_do = get_object_or_404(TODO, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        complete_to_do.date_completed = timezone.now()
        complete_to_do.save()
        return redirect('current_to_do')


@login_required
def delete_to_do(request, todo_pk):
    delete_to_do = get_object_or_404(TODO, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        delete_to_do.delete()
        return redirect('current_to_do')


@login_required
def completed_to_do(request):
    todolist = TODO.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completed_to_do.html', {'todolist': todolist})
