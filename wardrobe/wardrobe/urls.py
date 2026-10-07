"""
URL configuration for wardrobe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home,wardrobe,add_clothing,register,user_login,edit_clothing,delete_clothing,outfit_planner,create_outfit,edit_outfit, delete_outfit,profile,edit_profile,ClothingListCreateView,ClothingDetailView,OutfitListCreateView,OutfitDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns=[

    path('wardrobe/',wardrobe,name='wardrobe'),
    path('',home,name='home'),
    path('add-clothing/',add_clothing,name='add-clothing'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('edit-clothing/<int:id>/',edit_clothing,name='edit-clothing'),
    path('delete-clothing/<int:id>/',delete_clothing,name='delete-clothing'),
    path('outfit-planner/',outfit_planner,name='outfit-planner'),
    path('create-outfit/',create_outfit,name='create-outfit'),
    path('edit-outfit/<int:id>/',edit_outfit,name='edit-outfit'),
    path('delete-outfit/<int:id>/',delete_outfit,name='delete-outfit'),
    path('profile/',profile,name='profile'),
    path('edit-profile/',edit_profile, name='edit-profile'),
    path('admin/',admin.site.urls),
    path('token/',TokenObtainPairView.as_view(),name='token'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('clothing/',ClothingListCreateView.as_view(),name='clothing'),
    path('clothing/<int:pk>/',ClothingDetailView.as_view(),name='clothing-detail'),
    path('outfits/',OutfitListCreateView.as_view(),name='outfits'),
    path('outfits/<int:pk>/',OutfitDetailView.as_view(),name='outfit-detail'),

]         

if settings.DEBUG:
    urlpatterns+=static(
        settings.MEDIA_URL,document_root=settings.MEDIA_ROOT
    
    )

