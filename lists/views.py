from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()


def home_page(request: HttpRequest):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    form = None
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    else:
        form = ExistingListItemForm(for_list=list_)

    return render(request, 'list.html',
                  {'list': list_, 'form': form, })


def new_list(request: HttpRequest):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def my_lists(request: HttpRequest, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def list_share(request: HttpRequest, list_id):
    email = request.POST['shared_email']
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(email)

    messages.success(request, f'List shared with {email}')
    return redirect(list_)
