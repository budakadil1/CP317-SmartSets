from django.shortcuts import render, HttpResponse
from . models import Sets
from django.core.exceptions import ObjectDoesNotExist
from cards.models import Card
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CreateDeckForm
# Create your views here.
def index(request):
    return render(request, "index.html")

def search_sets(request):
    query = request.GET.get('q')
    match_sets = Sets.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    set_count = len(match_sets)

    context = {"sets":match_sets, "count":set_count}
    return render(request, "view_sets.html", context=context)

def view_sets(request):
    # return all sets here
    all_sets = Sets.objects.all()
    
    set_count = len(all_sets)

    context = {"sets":all_sets, "count":set_count}
    return render(request, "view_sets.html", context=context)

def view_single_set(request, slug):
    try:
        match_set = Sets.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return render(request, "no_resource.html")
        
    matched_cards = Card.objects.filter(owner_set=match_set)
    context = {"matched_set": match_set, "cards":matched_cards}
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
            # grab cleaned
            print(form.cleaned_data)
    else:
        form = CreateDeckForm()
    return render(request, 'create_set.html', {'form':form})
