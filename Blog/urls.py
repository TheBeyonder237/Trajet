from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('solution/', solution, name="solution"),
    path('demo/', demo, name="demo"),
    path('portfolio/', portfolio, name="portfolio"),
    path('code/', code, name="code"),
    path('contribution/', contribution, name="contribution"),
    path('login/', login, name="login"),
]
