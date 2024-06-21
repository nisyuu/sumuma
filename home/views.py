from django.views import generic


class Top(generic.TemplateView):
    template_name = 'home/top.html'


class TermsOfService(generic.RedirectView):
    url = 'https://alwaysblue.notion.site/4117c20f7d4149fb90dde04989be0299'
    permanent = True


class PrivacyPolicy(generic.RedirectView):
    url = 'https://alwaysblue.notion.site/842a8798e57d4bc3ac0961ed1d664ff7'
    permanent = True

