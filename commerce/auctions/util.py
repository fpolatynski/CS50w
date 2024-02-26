from .models import Bid, Listing, User


# Check if listing_id is in user watchlist
def is_in_watchlist(user_id: int, listing_id: int) -> bool:
    w = User.objects.get(pk=user_id).watchlist.filter(pk=listing_id)
    if w:
        return True
    else:
        return False


# Get highest listing bid id
def get_highest_bid_author(listing_id: int, user: User) -> User:
    bid = Bid.objects.filter(bid_on_id=listing_id).order_by('amount').reverse().first()
    if bid:
        return bid.author
    else:
        return Listing.objects.get(pk=listing_id).listing_owner
