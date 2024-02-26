from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User, Listing, Comment, Bid
from .util import is_in_watchlist, get_highest_bid_author


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_closed=False)
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
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


# Create Form from class Listing to give user ability to create listing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'min_bid', 'image_url', 'category', 'description']
        widgets = {
            'description': forms.Textarea()
        }


@login_required
def create(request):
    if request.method == 'POST':
        # Create Model form object from provided data
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            # Adding owner
            new_listing.listing_owner = User.objects.get(pk=request.user.id)
            new_listing.current_biggest_bid = form.cleaned_data['min_bid']
            new_listing.save()
            # Save Many to many data
            form.save_m2m()

            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })


def listing(request, listing_id):
    if request.method == 'POST':
        action = request.POST.get("listing_to_watchlist", None)
        to_make_bid = int(request.POST.get("bid_value", 0))
        closure = request.POST.get("closure", None)

        if action:
            # Add listing with listing_id to user watchlist
            listing_to_add = Listing.objects.get(pk=listing_id)
            if action == "add":
                listing_to_add.watchlist.add(User.objects.get(pk=request.user.id))
            elif action == "remove":
                listing_to_add.watchlist.remove(User.objects.get(pk=request.user.id))

        if to_make_bid:
            # Add bid to database
            print("TODO: 1")
            if to_make_bid > Listing.objects.get(pk=listing_id).current_biggest_bid:
                bid = Bid(amount=to_make_bid, author_id=request.user.id, bid_on_id=listing_id)
                bid.save()
                # Changing listing biggest bid
                lst = Listing.objects.all().get(pk=listing_id)
                lst.current_biggest_bid = to_make_bid
                lst.save()
            else:
                # Bid too Low
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=listing_id),
                    "watchlist": is_in_watchlist(request.user.id, listing_id),
                    "comments": Comment.objects.filter(comment_on_id=listing_id),
                    "listing_winner": get_highest_bid_author(listing_id, request.user),
                    "error": True
                })
                pass
        if closure:
            # After closure of listing
            lst = Listing.objects.get(pk=listing_id)
            lst.is_closed = True
            lst.save()

    if request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
            "watchlist": is_in_watchlist(request.user.id, listing_id),
            "comments": Comment.objects.filter(comment_on_id=listing_id),
            "listing_winner": get_highest_bid_author(listing_id, request.user)
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=listing_id),
        })


@login_required
def add_comment(request, listing_id):
    # CommentForm
    if request.method == 'POST':
        text = request.POST.get("text", None)
        print(text)
        if text:
            new_comment = Comment(text=text, writer=request.user, comment_on_id=listing_id)
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))
    else:
        return render(request, "auctions/add_comment.html", {
            'listing': Listing.objects.get(pk=listing_id)
        })


@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(watchlist=request.user)
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.CATEGORIES_CHOICES
    })


def display_category(request, category_id):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category_id)
    })
