from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create-listing", views.create_listing, name="create_listing"),
    path("submit-listing", views.submit_listing, name="submit_listing"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),

    path("<int:listing_id>", views.display_listing, name="display_listing"),
    path("<int:listing_id>/new-bid",views.new_bid, name="new_bid"),
    path("<int:listing_id>/close-auction",views.close_auction, name="close_auction"),
    path("<int:listing_id>/add-watchlist",views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>/remove-watchlist",views.remove_watchlist, name="remove_watchlist"),
    path("<int:listing_id>/add-comment",views.add_comment, name="add_comment"),
    
]
