from datetime import datetime

from django.shortcuts import render,redirect
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rango.models import Category, Page, UserProfile
from rango.forms import PageForm, CategoryForm, UserProfileForm,UserForm
from rango.bing_search import run_query


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            try:

                form.save(commit=True)

                return index(request)
            except IntegrityError as e:
                return form.errors.add_error('name', 'This category already exists.')
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


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

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict = {'boldmessage': "This tutorial was made by Rhianna Scott, 2084246S"}
    context_dict['visits'] = count

    # remember to include the visit data

    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        try:
            query = request.POST['query'].strip()

            if query:
                # Run our Bing function to get the results list!
                result_list = run_query(query)

                context_dict['result_list'] = result_list
                context_dict['query'] = query
        except:
            pass

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)



def register_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            if request.user.is_authenticated():
                profile = profile_form.save(commit=False)
                user = User.objects.get(id=request.user.id)
                profile.user = user
                try:
                    profile.picture = request.FILES['picture']
                except:
                    pass
                profile.save()
                return index(request)
    else:
        form = UserProfileForm(request.GET)
    return render(request, 'rango/profile_registration.html', {'profile_form': form})

@login_required
def profile(request):
    u = User.objects.get(username=request.user.username)
    context_dict = {}

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render(request, 'rango/profile.html', context_dict)

@login_required
def edit_profile(request):
    if request.method == 'POST':

        users_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(request.POST, instance=users_profile)
        if profile_form.is_valid():
            profile_to_edit = profile_form.save(commit=False)
            try:
                profile_to_edit.picture = request.FILES['picture']
            except:
                pass
            profile_to_edit.save()
            return profile(request)
    else:
        form = UserProfileForm(request.GET)
        return render(request, 'rango/edit_profile.html', {'profile_form': form})


def users(request):
    context_dict = {}
    profiles = UserProfile.objects.all()
    context_dict['profiles'] = profiles
    return render(request, 'rango/users.html', context_dict)


def view_profile(request, profile_name):
    context_dict = {}
    user = User.objects.get(username=profile_name)
    context_dict['user'] = user
    profile = UserProfile.objects.get(user=user)
    context_dict['profile'] = profile
    return render(request, 'rango/view_profile.html', context_dict)
