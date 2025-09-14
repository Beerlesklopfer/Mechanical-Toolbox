from django.views.generic import TemplateView

class AppTemplateMixin:
    app_name: str = None  # kann überschrieben werden
    
    def get_app_name(self):
        # Falls app_name gesetzt ist -> nimm den
        if self.app_name and self.app_name != "index.html":
            return self.app_name
        #aus dem kontext holen (z.B. aus urls.py)
        if 'app_name' in self.kwargs:
            return self.kwargs['app_name']
        # wenn instanz view attribut app_name hat, dann von dort holen
        if hasattr(self, 'app_name') and self.app_name:
            return self.app_name
        print(self.app_name)
        # ansonsten aus template_name extrahieren (z. B. "tolerances/index.html")
        return ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = self.get_app_name()
        context["app_name"] = app
        context["app_title"] = app.capitalize() if app else "Mechanical Toolbox"
        context['toolbar_partial'] = "partials/toolbar.html"
        context["sheet_partial"] = "partials/sheet.html"
        context['footer_partial'] = "partials/footer.html"
        context["calculation_partial"] = f"{app}/partials/calculation.html"
        context["standards_partial"] = f"{app}/partials/standards.html"
        context["hints_partial"] = f"{app}/partials/hints.html"
        context["examples_partial"] = f"{app}/partials/examples.html"
        context["exercises_partial"] = f"{app}/partials/exercises.html"
        return context
