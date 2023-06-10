from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/watch", views.watch, name="AddTo_watchlist"),
    path("<int:listing_id>/unwatch", views.unwatch, name="RemoveFrom_watchlist"),
    path("myWatchlist", views.myWatchlist, name="myWatchlist_url"),
    path("<int:listing_id>/comment", views.comment, name="addCommenturl"),
    path("<int:listing_id>/bid", views.bid, name="bidurl"),
    path("<int:listing_id>/close", views.closeAuction, name="closeurl"),
    path("by_categories", views.listings_by_categories, name="categoriesurl"),
    path("by_categories/<str:category>", views.listings_by_category, name="categoryurl"),
    path("won", views.auctions_won, name="wonurl"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#below was coded for ImageField



