from django.conf.urls import patterns, url
from django.contrib import admin
from functools import update_wrapper
from .models import Employer
from .forms import EmployerCreationWizard


class EmployerAdmin(admin.ModelAdmin):
    def get_urls(self):
        """Override the default "add" view with the employer creation wizard."""


        info = self.model._meta.app_label, self.model._meta.model_name
        urlpatterns = patterns(
            '',
            url(
                r'^add/$',
                EmployerCreationWizard.as_view(),
                name='%s_%s_add' % info
            ),
        )
        urlpatterns += super(EmployerAdmin, self).get_urls()
        return urlpatterns

    def changelist_view(self, request, extra_context=None):
        import ipdb; ipdb.set_trace()
        return super(EmployerAdmin, self).changelist_view(request, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        import ipdb; ipdb.set_trace()
        super(EmployerAdmin, self).add_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        import ipdb; ipdb.set_trace()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        import ipdb; ipdb.set_trace()

admin.site.register(Employer, EmployerAdmin)

