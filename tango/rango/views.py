from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})

from rango.forms import PageForm

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    views_list =  Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'view': views_list}
    return render(request,'rango/index.html',context_dict)

def about(request):
    context_dict = {'boldmessage':"This tutorial was made by Rhianna Scott, 2084246S" }
    return render(request,'rango/about.html',context_dict)



def category(request, category_name_slug):
    context = RequestContext(request)
    category_name = decode_url(category_name_slug)
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:

        pass
    return render(request, 'rango/category.html', context_dict)