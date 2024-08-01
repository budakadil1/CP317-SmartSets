from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateCardForm
from sets.models import Sets
from django.db.models import Q, F
from .models import Card
# Create your views here.
@login_required
def add_card(request, slug):
    if request.method == 'POST':
        # check if user owns the current set
        # try and get the object first
        deck = Sets.objects.filter(Q(author=request.user) | Q(shared_with=request.user))
        form = CreateCardForm(request.POST)
        
        if form.is_valid():
            Sets.objects.filter(slug=form.instance.owner_set.slug).update(card_count=F("card_count")+1)
            print(form.instance.owner_set.card_count)
            form.save()
            return redirect('view_set', form.instance.owner_set.slug)
        else:
            return render(request, 'create_set.html', {'form':form})
    else:
        deck = Sets.objects.filter((Q(author=request.user) | Q(shared_with=request.user)))
        if(len(deck) == 0):
            return render(request, 'no_resource.html')
        slug_deck = deck.filter(slug=slug)
        if(len(slug_deck) == 0):
            return render(request, 'no_resource.html')
        form = CreateCardForm(initial={'owner_set':slug_deck[0]})
        form.fields['owner_set'].queryset = deck
        form.fields['owner_set'].initial = slug_deck
        
    return render(request, 'create_card.html', {'form':form, 'title':'Add Card'})

def edit_card(request, slug):
    if slug:
        try:
            card = Card.objects.get(id=slug)
            card_owner_set = card.owner_set
            print(card_owner_set)
        except:
            return render(request, 'no_resource.html')
        if request.method == 'GET':
            form = CreateCardForm(instance = card)
            return render(request, 'create_card.html', {'form':form, 'title':'Edit Card'})
        else:
            form = CreateCardForm(request.POST, instance = card)
            print(card.owner_set.slug)
            print(form.instance.owner_set)
            if form.instance.owner_set.slug != card.owner_set.slug:
                print("I was changed!!!")
            if form.is_valid():
                form.save()
                if form.instance.owner_set != card_owner_set:
                    # form changed owner set so increase new owner set
                    Sets.objects.filter(slug=form.instance.owner_set.slug).update(card_count=F("card_count")+1)
                    Sets.objects.filter(slug=card_owner_set.slug).update(card_count=F("card_count")-1)

                return redirect('edit_cards', form.instance.owner_set.slug)
            else:
                print("WHAT THE FUCK")
    else:
        return render(request, "no_resource.html")
    
def remove_card(request, slug):
    if slug:
        try:
            card = Card.objects.get(id=slug)
            Sets.objects.filter(slug=card.owner_set.slug).update(card_count=F("card_count")-1)
            card.delete()
        except Exception as e:
            print(e)
            return render(request, 'no_resource.html')
    return redirect(request.META.get('HTTP_REFERER'))