"""askcats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='askcats_index'),
    path('index/<str:tag>/', views.index_by_tag, name='askcats_index_by_tag'),
    path('hot/', views.index_hot, name='askcats_hot'),  
    path('ask/', views.ask, name='askcats_ask'),
    path('login/', views.login, name='askcats_login'),
    path('signup/', views.signup, name='askcats_signup'),
    path('logout/', views.logout, name='askcats_logout'),
    path('question/<int:no>/', views.question_page, name='askcats_question'),
    path('settings/', views.settings, name='askcats_settings'),
    path('vote/', views.vote, name='askcats_vote'),
    path('correct/', views.correct, name='askcats_correct'),
    path('', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
