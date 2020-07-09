from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from djgeojson.views import GeoJSONLayerView
from . import views
from .models import Event
from .views import EventCreate, EventUpdate, EventDetail, EventList, EventMap, signup, PaperCreate, PaperUpdate, PaperDetail, PaperList, UserDetailView, UpdateUserView, UserCreateView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
    path('about', TemplateView.as_view(template_name='about.html'),
    name='about'),
    #url(r'^admin/', admin.site.urls),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    #path('users/(?P<userid>\d+)/$', search.views.user_detail, name='user_detail'), 
    path('users/<int:pk>/edit/', UpdateUserView.as_view(), name='user_update'),
    path('password_reset_form/', auth_views.PasswordChangeView.as_view()),
    path('users/logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('', EventMap.as_view(), name='index'),
    path('', EventMap.as_view(), name='home'),
    path('event/', EventList.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('event/<int:pk>/edit/', EventUpdate.as_view(), name='event_edit'),
    path('event/new/', EventCreate.as_view(), name='event_new'),
    path('paper/', PaperList.as_view(), name='paper_list'),
    path('paper/<int:pk>/', PaperDetail.as_view(), name='paper_detail'),
    path('paper/<int:pk>/edit/', PaperUpdate.as_view(), name='paper_edit'),
    path('paper/new/', PaperCreate.as_view(), name='paper_new'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model = Event, properties=('title', 'city', 'date')), name='data')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)