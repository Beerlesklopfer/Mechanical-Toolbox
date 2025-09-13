from django.contrib import admin
from django.urls import path, include
from .views import HomeView, ProfileView
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('accounts/signup/', ProfileView.as_view(), name='signup'),
    path("about/", TemplateView.as_view(template_name="about.html")),
]

# Optionally include app URLs if they are installed
optional_apps = [
    ('fasteners', 'fasteners'),
    ('fits', 'fits'),
    ('bearings', 'bearings'),
    ('gears', 'gears'),
    ('springs', 'springs'),
    ('shafts', 'shafts'),
    ('couplings', 'couplings'),
    ('tolerances', 'tolerances'),
]

for app_name, namespace in optional_apps:
    if app_name in settings.INSTALLED_APPS:
        urlpatterns.append(
            path(f'{app_name}/', include((f'{app_name}.urls', app_name), namespace=namespace))
        )