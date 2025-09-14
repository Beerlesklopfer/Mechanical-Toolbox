from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from main import settings as settings
from django.urls import reverse
from .mixins import AppTemplateMixin

class HomeView(AppTemplateMixin, TemplateView):
    template_name = 'home.html'
    footer_partial = 'partials/footer.html'  # Define the attribute or set it appropriately

    
    def get(self, request):
        print("GET request received", self.footer_partial)
        # 'fits',                # Fits components
        # 'fasteners',           # Fasteners components
        # 'tolerances',          # Tolerances components
        # 'bearings',            # Bearings components
        # 'gears',               # Gears components
        # 'springs',             # Springs components
        # 'shafts',              # Shafts components
        # 'couplings',           # Couplings components
        # 'utils',               # Shared utilities

        machinery_elements = [
        {
                'title': 'Passungen nach DIN ISO 286',
                'app': 'fits',
                'description': 'Passungen nach DIN ISO 286',
                'icon': 'fa-solid fa-circle-nodes',
                'color': 'bg-primary',
                'endpoint': 'index'
            },
           {
                'title': 'Toleranzen',
                'app': 'tolerances',
                'description': 'Wälzlager, Gleitlager und andere Lagertypen',
                'icon': 'fa-solid fa-cog',
                'color': 'bg-success',
                'endpoint': 'index'
            },
        {
                'title': 'Befestigungselemente',
                'app': 'fasteners',
                'description': 'Schrauben, Muttern, Unterlegscheiben und andere Verbindungselemente',
                'icon': 'fa-solid fa-bolt',
                'color': 'bg-primary',
                'endpoint': 'index'
            },
           {
                'title': 'Lager',
                'app': 'bearings',
                'description': 'Wälzlager, Gleitlager und andere Lagertypen',
                'icon': 'fa-solid fa-cog',
                'color': 'bg-success',
                'endpoint': 'index'
            },
            {
                'title': 'Zahnräder',
                'app': 'gears',
                'description': 'Stirnräder, Kegelräder, Schraubenräder und Getriebeberechnung',
                'icon': 'fa-solid fa-gear',
                'color': 'bg-info',
                'endpoint': 'index'
            },
            {
                'title': 'Federn',
                'app': 'springs',
                'description': 'Druckfedern, Zugfedern, Torsionsfedern und Federberechnung',
                'icon': 'fa-solid fa-sliders',
                'color': 'bg-warning',
                'endpoint': 'index'
            },
            {
                'title': 'Wellen und Achsen',
                'app': 'shafts',
                'description': 'Berechnung und Auslegung von Wellen und Achsen',
                'icon': 'fa-solid fa-arrows-up-down-left-right',
                'color': 'bg-danger',
                'endpoint': 'index'
            },
            {
                'title': 'Kupplungen',
                'app': 'couplings',
                'description': 'Starre und elastische Kupplungen, Berechnung von Kupplungen',
                'icon': 'fa-solid fa-link',
                'color': 'bg-secondary',
                'endpoint': 'index'
            }
        ]
        
        for element in machinery_elements:
            element['installed'] = apps.is_installed(element['app'])
            print("{} is {}".format(element['title'], apps.is_installed(element['app'])) )

            if settings.DEBUG and element['installed']:
                messages.add_message(request, messages.INFO, "Machinery element {} is installed".format(element['title']))
        
        context = {
            'machinery_elements': machinery_elements,
            'page_title': 'Mechanical Toolbox - Maschinenelemente'
        }

        if request.headers.get('HX-Request'):
            context['hx_trigger'] = 'true'
            return render(request, 'partials/element_tiles.html', context)
        else:
            context['hx_trigger'] = 'false'
        return render(request, 'home.html', context)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Profil {self.request.user.username} - Mechanical Toolbox'
        context['username']   = self.request.user
        context['url']        = reverse('profile', kwargs={'username': self.request.user.username})
        return context

    def get(self, request, username=None):
        if username is None:
            username = request.user.username
        return super().get(request, username=username)