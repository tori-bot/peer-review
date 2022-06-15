from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_project/', views.upload_project, name='upload_project'),
    path('project_update/<project_id>',views.project_update,name='project_update'),
    path('delete_project/<project_id>',views.delete_project,name='delete_project'),

    path('single_project/<int:pk>/',views.single_project, name='single_project'),
    path('add_comment/<int:project_id>/',views.comment, name='comment'),

    path('profile_form/<int:id>/', views.profile_form, name='profile_form'),
    path('profile/', views.profile, name='profile'),
    path('user_profile/<str:username>/',
         views.user_profile, name='user_profile'),

    path('technology/', views.technology, name='technology'),
    path('art/', views.art, name='art'),
    path('fashion/', views.fashion, name='fashion'),
    path('architecture/', views.architecture, name='architecture'),

    path('api/projects/',  views.ProjectView.as_view(), name='projects'),
    path('api/profiles/',  views.ProfileView.as_view(), name='profiles'),
    path("api", views.ApiList.as_view(), name="api"),

    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
