from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),

    path('profile_form/<int:id>/',views.profile_form,name='profile_form'),
    path('profile/',views.profile,name='profile'),

    path('search/',views.search, name='search'),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)