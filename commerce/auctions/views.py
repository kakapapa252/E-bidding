from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse
from django.db.models import Max
from .models import *

from .forms import CreateForm, BidForm, CommentForm

from django.contrib import messages




def index(request):
    listings = Listing.objects.all().order_by("-listing_date").filter(active = True)
    return render(request, "auctions/index.html", context={"listings":listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.created_by = request.user 

            commit = commit.save()
            messages.success(request, f"Created!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Error Detected")
            return HttpResponseRedirect(reverse("create"))

    form = CreateForm
    return render(request, "auctions/create.html", context={"form": form})


def item_page(request,idx):
    item = get_object_or_404(Listing,idx=idx)
    user = request.user
    form = BidForm
    comment_form = CommentForm

    comments = CommentList.objects.filter(item=item)

    max_bid = item.price
    max_bid_user = item.created_by
    existing_bids =  BiddingList.objects.filter(item=item)
    all_bids = [(i.bid, i.user) for i in existing_bids.all()]
    
    try:
        new_bid, new_bid_user = max(all_bids)
        if new_bid > max_bid:
            max_bid, max_bid_user = new_bid, new_bid_user
    except:
        pass
    
    
    number_bids = len(all_bids)
    #print(max_bid, max_bid_user)
    

    if request.method == "POST":
        form = BidForm(request.POST,)
        comment_form = CommentForm(request.POST,)
        if form.is_valid():
            bidding = form.save(commit=False)
            bidding.user = user
            bidding.item = item
            bidding.save()
            return render(request,"auctions/item_page.html", 
            context={"item":item, "form": form, "max_bid": max_bid, "max_bid_user": max_bid_user, 'number_bids':number_bids,"comment_form": comment_form, "comments": comments})
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.item = item
            comment.save()
            return render(request,"auctions/item_page.html", 
            context={"item":item, "form": form, "max_bid": max_bid, "max_bid_user": max_bid_user, 'number_bids':number_bids,"comment_form": comment_form, "comments": comments})

        else:
            print("error")
            return render(request,"auctions/item_page.html", 
            context={"item":item, "form": form, "max_bid": max_bid, "max_bid_user": max_bid_user, 'number_bids':number_bids,"comment_form": comment_form, "comments": comments})

    return render(request,"auctions/item_page.html", 
    context={"item":item, "form": form, "max_bid": max_bid, "max_bid_user": max_bid_user, 'number_bids':number_bids,"comment_form": comment_form, "comments": comments})


def my_created(request):
    try:
        user = request.user
        listings =  Listing.objects.filter(created_by=user)
        return render(request,"auctions/my_created.html", context={"listings":listings})
    except TypeError:
        return render(request,"auctions/not_auth.html")


def remove_from_created(request,idx):
    try:
        user = request.user
        created_item =  Listing.objects.get(idx=idx, created_by =user,)
        title = created_item.title
        created_item.delete()
        return HttpResponseRedirect(reverse("my_created"))
    except:

        return HttpResponseRedirect(reverse("my_created"))


def wishlist(request):
    try:
        user = request.user
        items =  Wishlist.objects.filter(user=user)
        new_list = [i.item.idx for i in items.all()]
        dates = [i.added_date for i in items.all()]
        listings = Listing.objects.in_bulk(new_list, field_name='idx')
        list_value = listings.values()

        listings_dates = list(zip(list_value,dates))
        return render(request,"auctions/wishlist.html", context={"items":listings_dates,})
    except TypeError:
        return render(request,"auctions/not_auth.html")


def remove_from_wishlist(request,idx):
    try:
        user = request.user
        item = get_object_or_404(Listing,idx=idx)
        title = item.title
        wished_item = Wishlist.objects.get(item=item, user =user,)
        wished_item.delete()
        messages.success(request, f"Removed: {title}")
        return HttpResponseRedirect(reverse("wishlist"))
    except:
        messages.error(request, f"Unable to remove item.")
        return HttpResponseRedirect(reverse("wishlist"))

def add_to_wishlist(request,idx):
    item = get_object_or_404(Listing,idx=idx)
    user = request.user
    wished_item,created = Wishlist.objects.get_or_create(item=item, user =user,)
    if created:
        
        wished_item.save()
    else:
        
        wished_item.save()

    print ('added',user,wished_item)
    return HttpResponseRedirect(reverse("wishlist"))


def category(request, cat):
    listings =  Listing.objects.filter(category = cat)
    return render(request,"auctions/category.html", context={"listings":listings, "cat": cat})


def deactive_listing_view(request):
    
    biddings = BiddingList.objects.select_related('item')
    listings = biddings.values("item").annotate(Max('bid')).order_by().filter(user=request.user)
    #listings = Listing.objects.in_bulk(new_list, field_name='idx')
    #listings = Listing.objects.all().order_by("-listing_date").filter(active = False)
    print(biddings)
    print(listings)


    return render(request, "auctions/deactivate_list_view.html", context={"listings":listings})

def deactive(request, idx):
    try:
        user = request.user
        created_item =  Listing.objects.get(idx=idx, created_by =user,)
        
        created_item.active = False
        created_item.save()
        return HttpResponseRedirect(reverse("my_created"))
    except:

        return HttpResponseRedirect(reverse("my_created"))