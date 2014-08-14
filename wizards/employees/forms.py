from django import forms
from django.forms import fields, models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.utils.encoding import force_unicode
from .models import Employer


class ContactForm(forms.Form):
    first_name = fields.CharField(max_length=50, label="Contact's first name")
    last_name = fields.CharField(max_length=50, label="Contact's last name")
    email = fields.EmailField(label="Contact's email address")


class EmployerForm(models.ModelForm):
    class Meta:
        model = Employer
        exclude = ('user',)


class EmployerCreationWizard(SessionWizardView):

    form_list = [UserCreationForm, ContactForm, EmployerForm]
    """
    FormWizard, representing the employer creation process.

    To add a new employer to the database, we'll need to:

     1. Choose a username and password, which the employer'll use to login.
        Make sure we verify the password by entering it twice.
     2. Enter the name and email address of the contact person for this employer.
     3. Enter the company name, address and website

    Each of these steps is handled by an appropriate form; the "done" method
    uses the data collected to create the employer.
    """
    @property
    def __name__(self):
        # Python instances don't define __name__ (though functions and classes do).
        # We need to define this, otherwise the call to "update_wrapper" fails:
        return self.__class__.__name__

    def get_template(self, step):
        # Optional: return the template used in rendering this wizard:
        return 'admin/testapp/employer/wizard.html'

    def get_context_data(self, form, **kwargs):
        context = super(EmployerCreationWizard, self).get_context_data(form=form, **kwargs)
        context['opts'] = Employer._meta
        from django.contrib.admin.helpers import AdminForm
        # Wrap this form in an AdminForm so we get the fieldset stuff:
        super_form = AdminForm(context['form'], [(
            'Step %d of %d' % (0 + 1, 2),
            {'fields': form.base_fields.keys()}
            )], {})
        context['super_form'] = super_form
        return context

    def parse_params(self, request, admin=None, *args, **kwargs):
        # Save the ModelAdmin instance so it's available to other methods:
        self._model_admin = admin
        # The following context variables are expected by the admin
        # "change_form.html" template; Setting them enables stuff like
        # the breadcrumbs to "just work":
        opts = admin.model._meta
        self.extra_context.update({
            'title': 'Add %s' % force_unicode(opts.verbose_name),
            # See http://docs.djangoproject.com/en/dev/ref/contrib/admin/#adding-views-to-admin-sites
            # for why we define this variable.
            'current_app': admin.admin_site.name,
            'has_change_permission': admin.has_change_permission(request),
            'add': True,
            'opts': opts,
            'root_path': admin.admin_site.root_path,
            'app_label': opts.app_label,
        })

    def render_template(self, request, form, previous_fields, step, context=None):
        from django.contrib.admin.helpers import AdminForm
        # Wrap this form in an AdminForm so we get the fieldset stuff:
        form = AdminForm(form, [(
            'Step %d of %d' % (step + 1, self.num_steps()),
            {'fields': form.base_fields.keys()}
            )], {})
        context = context or {}
        context.update({
            'media': self._model_admin.media + form.media
        })
        return super(EmployerCreationWizard, self).render_template(request, form, previous_fields, step, context)

    def done(self, request, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        # First, create user:
        user = User.objects.create(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        user.set_password(data['password1'])
        user.save()
        # Next, create employer:
        employer = Employer.objects.create(
            user=user,
            company_name=data['company_name'],
            address=data['address'],
            company_description=data.get('company_description', ''),
            website=data.get('website', '')
        )
        # Display success message and redirect to changelist:
        return self._model_admin.response_add(request, employer)
