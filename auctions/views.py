from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

from .models import *
from .forms import *
# categories= ["electronic",  "clothing", "tops", "bottoms", "shoes", "animal", "instrument", "toy", 
# "school supply", "furniture"]
# Instead a list, categories can be it's own model and and admin can add the the categories via django admin

def index(request):
    activeListings = Listing.objects.filter(active=True).all()
    return render(request, "auctions/index.html", {
        "active_auctions": activeListings})




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

@login_required(login_url='/login')
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
        #the following 2 lines where added. without it, a logged in user can still access the register view
        if request.user.is_authenticated:
            return render(request, "auctions/.html")
        else:
            return render(request, "auctions/register.html")

@login_required(login_url='/login')
def new_listing(request):
    if request.method == "POST":
        form=ListingForm(request.POST, request.FILES) #this gets all the inputs user submitted in the form. .FILES is the media submissions like images submitted.
        if form.is_valid():
            print("valid form")
            if float(form.instance.current_bid) < 0.00:
                messages.warning(request, "Minimum starting bid is $0.00.")
                return render(request, "auctions/new_listing.html", {
                "form": form
            })
            # form.instance.image same as request.POST.get("image")
            # if form.instance.image:
            #     print("there's an image!")
            form.instance.seller=request.user
            
            #no need to declare a new Listing() and then save each individual user input on the form as a Listing() attribute
            # this is because line 83 var_name = ListingForm(request.POST, request.FILES) informs Django that the user is completing a Listing Form
            # and ListingForm is based on the Listing Model
            # listing=Listing()
            # listing.seller=request.user
            # listing.list_item=request.POST.get("list_item")
            # listing.description=request.POST.get("description")
            # listing.current_bid=request.POST.get("current_bid")

            # if request.POST.get("categoryType"):
            #     cat = Category.objects.get(pk=request.POST.get("categoryType"))
            #     listing.categoryType=cat
                #listing.categoryType=request.POST.get("categoryType") THIS LINE DOES NOT WORK
                #listing.categoryType=Category.objects.get(category=request.POST.get("categoryType"))
            newListing = form.save() #this allows for saving the entire form inputs as a new model instance instead of saving each individual
            #print(newListing)
            # return render(request, "auctions/new_listing.html", {
            #     "message": "Please complete required fields."
            # })
            #direct user to the page of the newly listed item
        else:
            #print("Invalid Form")
            if not form.instance.list_item:
            #same as if not request.POST.get("list_item"):
                messages.warning(request, "Please provide a name for the listing.")
            if not form.instance.current_bid:
                messages.warning(request, "Please provide an amount.")
            return render(request, "auctions/new_listing.html", {
                "form": form,
            })

        return HttpResponseRedirect(reverse("index"))

    #if not POST, render a ListingForm
    return render(request, "auctions/new_listing.html", {
        "form": ListingForm()
    })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    #current_user=request.user
    #usersWatchlist = current_user.watched.all()
    if request.user.is_authenticated: 
        watched = Watchlist.objects.filter(user=request.user, listing=listing).exists
    else:
        #if watched is not defined there will be error:
        # cannot access local variable 'watched' where it is not associated with a value bc nothing is passed to watched in the context below
        watched = None
    comments = listing.allComments.all()
    #minimum bid must be greater than current_bid
    minBid = float(listing.current_bid)
    minBid = round(minBid+float(.01),2) #to avoid floating point "error"
    return render(request, "auctions/listing.html", {
         "selectedListing": listing,
         "form": CommentForm(),
         "allComments_forListing": comments,
         "minBid": minBid,
         "watched": watched,
    })
    
@login_required(login_url='/login')
def watch(request, listing_id):
    if request.method == "POST":
        listing= Listing.objects.get(id=listing_id)
        #watch_listing=Watchlist()
        # watch_listing.user = request.user
        # watch_listing.listing = listing
        listing_watched, is_created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
        if is_created == False:
            messages.warning(request, 'Already added to watchlist')
            #messages per https://stackoverflow.com/questions/58228681/how-to-display-error-message-in-django-template-after
            url = reverse('listing', kwargs={'listing_id':listing_id})
            return HttpResponseRedirect(url)
            comments = listing.allComments.all()
            return render(request, "auctions/listing.html", {
            "selectedListing": listing,
            "message": "Already added to watchlist.",
            "allComments_forListing": comments,
            })

        current_user=request.user
        usersWatchlist = current_user.watched.all()
        url = reverse('listing', kwargs={'listing_id':listing_id})
        return HttpResponseRedirect(url)
        
    url = reverse('listing', kwargs={'listing_id':listing_id})
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def unwatch(request, listing_id):
    if request.method == "POST":
        listing= Listing.objects.get(id=listing_id)
        # if Watchlist.objects.filter(user=request.user, listing=listing).exists:
        #     print("This Listing is in your watchlist")
        #     url = reverse('listing', kwargs={'listing_id':listing_id})
        #     return HttpResponseRedirect(url)
        # else:
        #     print("This Listing is not in your watchlist")
        #     url = reverse('listing', kwargs={'listing_id':listing_id})
        #     return HttpResponseRedirect(url)
        try:
            Watchlist.objects.get(user=request.user, listing=listing).delete()
        except:
            print("Not on your watchlist")
            url = reverse('listing', kwargs={'listing_id':listing_id})
            return HttpResponseRedirect(url)
        else:
            print("Removed from your watchlist")
            url = reverse('listing', kwargs={'listing_id':listing_id})
            return HttpResponseRedirect(url)

    url = reverse('listing', kwargs={'listing_id':listing_id})
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def myWatchlist(request):
        current_user=request.user
        usersWatchlist = current_user.watched.all() 
        #see notes for explanation of queryset list
        queryset = []
        for item in usersWatchlist:
            queryset.append(Listing.objects.get(pk=item.listing_id))
        #print(Listing.objects.filter(seller=current_user).all())
        #print(Listing.objects.all().filter(watchers=current_user)
        return render(request, "auctions/watchlist.html", {
            "Listings_watchedbyUser":queryset
        })


@login_required(login_url='/login')
def comment(request, listing_id):
    url = reverse('listing', kwargs={'listing_id':listing_id})
    #url coded so that after user adds comments, django will call the listing url which will call view.listing
    if request.method == "POST":
        form = CommentForm(request.POST) #gets user's POST data. The POST data is for a CommentForm
        if form.is_valid():
            user = request.user
            listing = Listing.objects.get(id=listing_id)
            comment = Comment(user=user, listing=listing, comment=request.POST.get('comment'))
            #if the comment in the comment instance is an empty string, do no post the comment just redirect to listing
            if not comment.comment:
                return HttpResponseRedirect(url)
            comment.save()
            return HttpResponseRedirect(url)
    #is this necessary? i only created this view for POST requests, however if the view only has if request.method==POST, and the url is accessed via GET, it returns errors
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def bid(request, listing_id):
    if request.method == "POST":
        bid_amount = request.POST.get('bid_amount')
        #check if user submitted bid amount is valid
        #https://stackoverflow.com/questions/7767361/python-validate-currency
        bid_amountValid = re.match(r'\d+(?:\.\d{0,2})?$', bid_amount)
        if bid_amountValid:
            listing = Listing.objects.get(pk=listing_id)
            if listing.seller == request.user:
                #no longer appears to be an issue if the listing does not display a "Place Bid" form for the seller
                messages.warning(request, "You cannot place a bid on an item you're selling!")
                return redirect('listing', listing_id=listing_id)
            current_bid = float(listing.current_bid)
            placed_bid = float(request.POST.get('bid_amount'))
            if placed_bid>current_bid:
                listing.current_bid = placed_bid
                listing.highest_bidder = request.user
                listing.save(update_fields=['current_bid', 'highest_bidder'])
                messages.success(request, 'Your bid has been placed!')
                return redirect('listing', listing_id=listing_id)
        messages.warning(request, 'Invalid bid amount.')        
        return redirect('listing', listing_id=listing_id)

    return redirect('listing', listing_id=listing_id)


@login_required(login_url='/login')
def closeAuction(request, listing_id):
    if request.method == "POST":
            listing = Listing.objects.get(pk=listing_id)
            if listing.seller == request.user:
                listing.active = False
                listing.save(update_fields=['active'])
                return redirect('listing', listing_id=listing_id)
            
    return redirect('listing', listing_id=listing_id)


def listings_by_categories(request):
    #categoryListings = [] List was too complex
    activeListings = Listing.objects.filter(active=True).all()
    allCategories = Category.objects.all()
    #print(allCategories)
    #use related attribute
    for category in allCategories:
        #print(f"{category}: {category.listings.filter(active=True).all()}")
        #check if the category has any listings. if the queryset=0, then there are no listings and we won't need to display this category on the html
        if len(Listing.objects.filter(active=True, categoryType=category).all()) == 0:
            allCategories = allCategories.exclude(category=category)
    return render(request, "auctions/categories.html", {
            "allCategories": allCategories,
            "active_listings": activeListings,
            })

def listings_by_category(request, category):
    selected_category = Category.objects.get(category=category) #without this, next line will return error Field 'id' expected a number but got 'shirt', because categoryType is a fk in Listing
    activeListings = Listing.objects.filter(active=True, categoryType=selected_category).all()
    print(activeListings)
    return render(request, "auctions/category.html", {
        "Category": category,
        "active_listings": activeListings,
        })
        
@login_required(login_url='/login')        
def auctions_won(request):
    user = request.user
    wonAuctions = Listing.objects.filter(active=False, highest_bidder=user).all()
    return render(request, "auctions/won.html", {
            "wonAuctions": wonAuctions,
            })
