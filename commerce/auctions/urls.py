from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("item_page/<idx>", views.item_page, name="item_page"),
    path("my_created/", views.my_created, name="my_created"),
    path("remove_from_created/<idx>", views.remove_from_created, name="remove_from_created"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_to_wishlist/<idx>", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove_from_wishlist/<idx>", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("category/<cat>", views.category, name="category"),
    path("deactive_listing_view/", views.deactive_listing_view, name="deactive_listing_view"),
    path("deactive/<idx>", views.deactive, name="deactive"),
    
]
