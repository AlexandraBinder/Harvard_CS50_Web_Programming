from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Bid, Auction_Listing, Comment


def index(request):
    return render(request, "auctions/index.html")


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


def create_listing(request):
    return render(request, "auctions/create-listing.html")


def submit_listing(request):
    if request.method == 'POST':
        
        user = request.user

        name = request.POST['name']
        category = request.POST['category']
        description = request.POST['description']
        url_link = request.POST['url_link']

        # Directly generate a Bid object, asociate the user making the bid
        starting_bid = Bid(bid=int(request.POST['starting_bid']), user=user)
        starting_bid.save()

        # Create a new Auction_Listing object, associate it with user and bid
        listing = Auction_Listing(owner=user, bid=starting_bid ,  closed=False,\
                                    name=name, description=description, category=category, url=url_link )
        listing.save()

        # Once listing is created, return tu index page
        return HttpResponseRedirect(reverse("index"))
    
    # else, aske to create a new listing
    return render(request, "auctions/create-listing.html")
    

def display_listing(request, listing_id):

    user = request.user

    if user.is_authenticated:
        
        listing = Auction_Listing.objects.get(pk=listing_id)

        comments = listing.comments.all()

        if request.user == listing.owner:
            is_owner = True
        else:
            is_owner = False

        listing_in_watchlist = request.user.watch_listings.all()

        return render(request, "auctions/display-listing.html", {
            "listing": listing,
            "comments": comments,
            "owner": is_owner,
            "listing_in_watchlist": listing_in_watchlist
        })
    else:
        return HttpResponseRedirect(reverse("index"))


def category(request):

    if request.method == 'POST':
        # Get chosen category
        categ = request.POST['category']

        # Get listings which belong to chosen category
        listings = Auction_Listing.objects.filter(category=categ, closed=False)

        return render(request, "auctions/index.html",{
            "active_listings": listings
        })
    

def close_auction(request, listing_id):

    listing = Auction_Listing.objects.get(pk=listing_id)
    listing.closed = True
    listing.save()

    return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))


def watchlist(request):

    user = request.user

    if user.is_authenticated:

        users_watchlist = user.watch_listings.all()

        return render(request, "auctions/watchlist.html",{
            "users_watchlist": users_watchlist
        })
    
    else:
        return HttpResponseRedirect(reverse("index"))


def add_watchlist(request, listing_id):
    
    # adds user to watchlist
    user = request.user
    listing = Auction_Listing.objects.get(pk=listing_id)
    listing.watchlist.add(user)
    
    return HttpResponseRedirect(reverse("display_listing",args=(listing_id,)))


def remove_watchlist(request, listing_id):
    
    user = request.user
    listing = Auction_Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))

def new_bid(request, listing_id):
    
    listing = Auction_Listing.objects.get(pk=listing_id)
    new_bid = int(request.POST["new_bid"])
    
    # We use the foreign key to get the current bid value
    # We access the bid attribute from the listing object, 
    # which is associated to a Bid object with a bid attribute
    current_bid = listing.bid.bid 
    
    if new_bid > current_bid:
        # create new bid
        updated_bid = Bid(bid=new_bid, user=request.user)
        updated_bid.save()

        # associate new bid to listing
        listing.bid = updated_bid
        listing.save()

        return render(request,"auctions/display-listing.html", {
            "listing": listing,
            "message": "Your Bid was added successfully.",
            "updated": True,
            })

    else:
        return render(request,"auctions/display-listing.html",{
            "listing": listing,
            "message": "Sorry, your bid is not high enough.",
            "updated": False,
            })


def add_comment(request, listing_id):

    if request.method == "POST":
        
        # get data
        user = request.user
        text = request.POST["comment"]
        listing = Auction_Listing.objects.get(pk=listing_id)

        # create new comment object
        new_comment = Comment(text=text, writer=user, listing=listing)
        new_comment.save()

        return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))