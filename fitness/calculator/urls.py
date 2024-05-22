from . import views
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('', views.index, name='home'),
    path('one-rep-maximum/', views.one_rep_maximum, name='one-rep-maximum'),
    path('daily-calories-intake/', views.daily_calories_intake, name='daily-calories-intake'),
    path('profile/', csrf_exempt(views.profile_view), name='profile'),
    path('register/', views.register_view.as_view(), name="register"),
    # path('add-products/', views.my_func),
    path('my-nutrition/', views.my_nutrition, name='my-nutrition'),
    path('category/<slug:cat_slug>', views.category, name='category'),
    path('categories/', views.categories, name='categories'),
    path('product/<int:productid>/', views.product, name='product'),
    path('search_products/', views.search_products, name='search_products')
]
