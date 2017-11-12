from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Item, List


def home_page(request: HttpRequest):
    return render(request, 'home.html')


def view_list(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request: HttpRequest):
    text = request.POST['item_text']
    list_ = List.objects.create()
    Item.objects.create(text=text, list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    text = request.POST['item_text']
    Item.objects.create(text=text, list=list_)
    return redirect(f'/lists/{list_.id}/')
