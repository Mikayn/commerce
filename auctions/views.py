from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .formclasses import *


def index(request):
    listings = AuctionListing.objects.all().prefetch_related("categories").select_related("user")
    
    for listing in listings:
        highest_bid = listing.auction_bids.order_by('-bid_amount').first()
        listing.highest_bid = highest_bid.bid_amount if highest_bid else None
        
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next")

            if next_url:
                return HttpResponseRedirect (next_url)
            else:
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

@login_required
def CreateAuction(request):

    if request.method == "POST":
        auction_form = Create (request.POST)
        
        if auction_form.is_valid(): 
            try:
                obj = auction_form.save(commit= False)
                if not obj.image:
                    obj.image = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.istockphoto.com%2Fvectors%2Fno-image-available-sign-vector-id1138179183%3Fk%3D6%26m%3D1138179183%26s%3D612x612%26w%3D0%26h%3DprMYPP9mLRNpTp3XIykjeJJ8oCZRhb2iez6vKs8a8eE%3D&f=1&nofb=1&ipt=66661365c336cc251c77d7b9252e2cebde8b96d368f0061bbfda5d96ed5f485c"
                    
                obj.user = request.user
                
                obj.save()

                auction_form.save_m2m()

                return HttpResponseRedirect (reverse ('index'))
            
            except Exception as e:
                print("Exception(s): ", e)
        
        else:
            print("Not valid")
            print(auction_form.errors)

    else:    
        auction_form = Create()
    
    return render(request, "auctions/create.html", {
        "form": auction_form
    })

@login_required
def wishlist(request): 
    pass

@login_required
def categories(request):
    pass

def listing(request, id):
    
    listing = AuctionListing.objects.get(id = id)
    bids_num = listing.auction_bids.count()
    comments = listing.auction_comments.all()

    if listing.auction_bids.all():
        highest_bid = listing.auction_bids.order_by("-bid_amount").first()
    
    else:
        highest_bid = listing.starting_bid

    if request.method == "POST":

        bid_form = Bids(request.POST)
        comment_form = Comments(request.POST)

        if bid_form.is_valid():
            if float(request.POST.get ("bid_amount")) < float(highest_bid):

                messages.error (request, "Your bid cannot be lower than current bid! ")
                return redirect ("listing", id=id)
            
            obj = bid_form.save(commit= False)

            obj.user = request.user
            obj.auction_listing = listing
            obj.save()

            messages.success (request, "Bid Successful! ")
            return redirect ("listing", id = id)

        if comment_form.is_valid():
            obj = comment_form.save(commit= False)

            obj.user = request.user
            obj.auction_listing = listing
            obj.save()

            messages.success (request, "Comment posted successfully! ")
            return redirect ("listing", id = id)

    else:
        bid_form = Bids()
        comment_form = Comments()    

    return render (request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid": highest_bid,
        "bids_num": bids_num,
        "comments": comments,
        "bid_form": bid_form,
        "comment_form": comment_form,
    })