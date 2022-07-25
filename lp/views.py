from django.views import generic


class General(generic.TemplateView):
    template_name = 'lp/general.html'
