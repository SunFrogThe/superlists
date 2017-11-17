from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List


def home_page(request: HttpRequest):
    return render(request, 'home.html')


def view_list(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request: HttpRequest):
    text = request.POST['item_text']
    list_ = List.objects.create()
    item = Item(text=text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request: HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    text = request.POST['item_text']
    Item.objects.create(text=text, list=list_)
    return redirect(f'/lists/{list_.id}/')
