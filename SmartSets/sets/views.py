from django.shortcuts import render, HttpResponse, redirect
from . models import Sets
from django.core.exceptions import ObjectDoesNotExist
from cards.models import Card
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CreateDeckForm
from django.contrib import messages
from django.contrib.auth.models import User

# home page
def index(request):
    return render(request, "index.html")

# page to search sets
def search_sets(request):
    query = request.GET.get('q')
    query = "" if query == None else query
    match_sets = Sets.objects.filter((Q(name__icontains=query) | Q(description__icontains=query)) & Q(public=True))
    set_count = len(match_sets)

    context = {"sets":match_sets, "count":set_count}
    return render(request, "view_sets.html", context=context)

# page to browse all sets
def view_sets(request):
    # return all sets here
    if request.path == '/sets/':
        all_sets = Sets.objects.filter(public=True)
    else:
        all_sets = Sets.objects.all()
    
    set_count = len(all_sets)

    context = {"sets":all_sets, "count":set_count}
    return render(request, "view_sets.html", context=context)

# page to view single set
def view_single_set(request, slug):
    try:
        match_set = Sets.objects.get(slug=slug)
        if match_set.public == False:
            # check user permissions
            if request.user.is_authenticated:
                if match_set.author != request.user and match_set.shared_with.filter(username=request.user.username).exists() == False:
                    return render(request, "no_resource.html")
                
            else:
                return render(request, "no_resource.html")
    except ObjectDoesNotExist:
        return render(request, "no_resource.html")
    
    matched_cards = Card.objects.filter(owner_set=match_set)

    context = {"matched_set": match_set, "cards":matched_cards, "count": len(matched_cards)}
    return render(request, "view_single_set.html", context)

# page to view my sets
@login_required
def my_sets(request):
    try:
        query = request.user
        matched_sets = Sets.objects.filter(Q(author=query) | Q(shared_with=query))
    except:
        return render(request, "no_resource.html")
    
    set_count = len(matched_sets)
    context = {"sets":matched_sets, "count":set_count}

    return render(request, "view_sets.html", context=context)

# page to create sets
@login_required
def create_set(request):
    if request.method == 'POST':
        form = CreateDeckForm(request.POST)
        if form.is_valid():
            # grab shared with field
            form.instance.author = request.user
            form.instance.card_count = 0
            if request.POST['shared_with'] != "":
                try:
                    # get shared_with users delmiited by space
                    share_users_list = request.POST['shared_with'].split(' ')
                    share_users_objects = []
                    print(share_users_list)
                    for i in share_users_list:
                        if len(i) > 2:
                            share_user = User.objects.get(username=i)
                            if share_user == request.user:
                                messages.error(request, "You cannot share a set with yourself!")
                                return render(request, 'create_set.html', {'form':form})
                        share_users_objects.append(share_user)
                except ObjectDoesNotExist:
                    messages.error(request, "One of the username(s) could not be found! Please ensure that you entered the correct username!")
                    return render(request, 'create_set.html', {'form':form})
                
                form.save()
                try:
                    for i in share_users_objects:
                        form.instance.shared_with.add(i)
                except Exception as e:
                    print(e)
            else:
                form.save()
            return redirect('view_set', form.instance.slug)

        else:
            return render(request, 'create_set.html', {'form':form})
    else:
        form = CreateDeckForm()
    return render(request, 'create_set.html', {'form':form})

# page to edit sets
@login_required
def edit_set(request, slug):
    if slug:
            try:
                matched_set = Sets.objects.get(slug=slug)
            except ObjectDoesNotExist:
                return render(request, 'no_resource.html')
    else:
        return render(request, 'no_resource.html')
    if request.method == 'POST':
        form = CreateDeckForm(request.POST, instance=matched_set)
        if form.is_valid():
            # grab shared with field
            form.instance.author = request.user
            form.save()
            try:
                # get shared_with users delmiited by space
                share_users_list = request.POST['shared_with'].split(' ')
                share_users_objects = []
                print(share_users_list)
                for i in share_users_list:
                    if len(i) > 2:
                        share_user = User.objects.get(username=i)
                        if share_user == request.user:
                            messages.error(request, "You cannot share a set with yourself!")
                            return render(request, 'edit_set.html', {'form':form, 'set':matched_set})
                        share_users_objects.append(share_user)
            except ObjectDoesNotExist:
                messages.error(request, "One of the username(s) could not be found! Please ensure that you entered the correct username!")
                return render(request, 'edit_set.html', {'form':form, 'set':matched_set})
            form.instance.shared_with.clear()
            try:
                for i in share_users_objects:
                    form.instance.shared_with.add(i)
            except Exception as e:
                print(e)
            return redirect('view_set', form.instance.slug)
    else:   
            if request.user == matched_set.author:
                form = CreateDeckForm(instance=matched_set)                
                return render(request, 'edit_set.html', {'form':form, 'set':matched_set })
            else:
                return render(request, 'no_resource.html', {'custom':'You might not be the author of this set!'})
    
    return render(request, 'edit_set.html', {'form':form })

# page to delete sets
@login_required
def delete_set(request, slug):
    if slug:
        try:
            matched_set = Sets.objects.get(Q(author=request.user) | Q(slug=slug))
            matched_set.delete()
        except Sets.DoesNotExist:
            return render(request, 'no_resource.html')

    return redirect('my_sets')

# page to edit cards
@login_required
def edit_cards(request, slug):
    if slug:
            if request.method == 'GET':
                try:
                    matched_set = Sets.objects.get(slug=slug)
                    cards = Card.objects.filter(owner_set=matched_set)
                    context = {'cards':cards, 'slug':slug}
                    return render(request, 'edit_cards.html', context)
                except ObjectDoesNotExist:
                    return render(request, 'no_resource.html')
    else:
        return render(request, 'no_resource.html')

    return render(request, 'edit_set.html', {'slug': slug})