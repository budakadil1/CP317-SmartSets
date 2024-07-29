from django.shortcuts import render, HttpResponse, redirect
from . models import Sets
from django.core.exceptions import ObjectDoesNotExist
from cards.models import Card
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CreateDeckForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, "index.html")

def search_sets(request):
    query = request.GET.get('q')
    query = "" if query == None else query
    match_sets = Sets.objects.filter((Q(name__icontains=query) | Q(description__icontains=query)) & Q(public=True))
    set_count = len(match_sets)

    context = {"sets":match_sets, "count":set_count}
    return render(request, "view_sets.html", context=context)

def view_sets(request):
    # return all sets here
    if request.path == '/sets/':
        all_sets = Sets.objects.filter(public=True)
    else:
        all_sets = Sets.objects.all()
    
    set_count = len(all_sets)

    context = {"sets":all_sets, "count":set_count}
    return render(request, "view_sets.html", context=context)

def view_single_set(request, slug):
    try:
        match_set = Sets.objects.get(slug=slug)
        if match_set.public == False:
            # check user permissions
            if request.user.is_authenticated:
                if match_set.author != request.user and match_set.shared_with != request.user:
                    return render(request, "no_resource.html")
                
            else:
                return render(request, "no_resource.html")
    except ObjectDoesNotExist:
        return render(request, "no_resource.html")
    
    matched_cards = Card.objects.filter(owner_set=match_set)

    context = {"matched_set": match_set, "cards":matched_cards, "count": len(matched_cards)}
    return render(request, "view_single_set.html", context)

@login_required
def my_sets(request):
    try:
        query = request.user
        print(query)
        matched_sets = Sets.objects.filter(Q(author=query) | Q(shared_with=query))
    except:
        return render(request, "no_resource.html")
    
    set_count = len(matched_sets)
    context = {"sets":matched_sets, "count":set_count}

    return render(request, "view_sets.html", context=context)

@login_required
def create_set(request):
    if request.method == 'POST':
        form = CreateDeckForm(request.POST)
        if form.is_valid():
            # grab shared with field
            if request.POST['shared_with'] != "":
                try:
                    share_user = User.objects.get(username=request.POST['shared_with'])
                except ObjectDoesNotExist:
                    messages.error(request, "That username could not be found! Please ensure that you entered the correct username!")
                    return render(request, 'create_set.html', {'form':form})
                form.instance.shared_with = share_user
            form.instance.card_count = 0
            form.instance.author = request.user
            form.save(commit=True)
            return redirect('view_set', form.instance.slug)

        else:
            return render(request, 'create_set.html', {'form':form})
    else:
        form = CreateDeckForm()
    return render(request, 'create_set.html', {'form':form})


@login_required
def edit_set(request, slug):
    if slug:
            try:
                matched_set = Sets.objects.get(slug=slug)
                print(matched_set)
            except ObjectDoesNotExist:
                return render(request, 'no_resource.html')
    else:
        return render(request, 'no_resource.html')
    if request.method == 'POST':
        form = CreateDeckForm(request.POST, instance=matched_set)
        if form.is_valid():
            # grab shared with field
            if request.POST['shared_with'] != "":
                try:
                    share_user = User.objects.get(username=request.POST['shared_with'])
                except ObjectDoesNotExist:
                    messages.error(request, "That username could not be found! Please ensure that you entered the correct username!")
                    return render(request, 'create_set.html', {'form':form})
                form.instance.shared_with = share_user
            form.instance.author = request.user
            form.save(commit=True)
            return redirect('view_set', form.instance.slug)
    else:   
            if request.user == matched_set.author or request.user == matched_set.shared_with:
                form = CreateDeckForm(instance=matched_set)
            else:
                return render(request, 'no_resource.html')
    
    return render(request, 'edit_set.html', {'form':form})

@login_required
def edit_cards(request, slug):
    if slug:
            if request.method == 'GET':
                try:
                    matched_set = Sets.objects.get(slug=slug)
                    cards = Card.objects.filter(owner_set=matched_set)
                    context = {'cards':cards}
                    return render(request, 'edit_cards.html', context)
                except ObjectDoesNotExist:
                    return render(request, 'no_resource.html')
    else:
        return render(request, 'no_resource.html')
    
    
    return render(request, 'edit_set.html', {'form':form})