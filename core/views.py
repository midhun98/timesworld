from django.contrib.auth import login, authenticate
from django.shortcuts import render
from . import forms, models
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django import http
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout

def BASE(request):
    return render(request, 'base.html')


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.exists():
                    group = user.groups.all()[0].name
                    if group == "staff":
                        return http.HttpResponseRedirect(reverse('staff_view'))
                    elif group == "admin":
                        return http.HttpResponseRedirect(reverse('admin_view'))
                    elif group == "student":
                        return http.HttpResponseRedirect(reverse('student_view'))
                    elif group == "editor":
                        return http.HttpResponseRedirect(reverse('editor_view'))
                    else:
                        pass
                else:
                    return http.HttpResponseRedirect(reverse('base'))
    
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


class UserCreateView(generic.TemplateView):
    template_name = "user_create.html"

    def get_context_data(self, **kwargs):
        context ={}
        form = forms.UserCreateForm()
        sub_form = forms.ProfileCreateForm(self.request.user)
        context['form'] = form
        context['sub_form'] = sub_form
        return context

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)
        sub_form = forms.ProfileCreateForm(request.user, request.POST)
        if form.is_valid() and sub_form.is_valid():
            password = request.POST.get('password')
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            country = request.POST.get('country')
            mobile = request.POST.get('mobile')
            role = request.POST.get('role')

            roleobj = models.Role.objects.get(id=role)

            user = User(username=username, first_name=first_name, last_name=last_name, email=email, is_staff=True)
            user.set_password(password)
            user.save()
            user.groups.add(roleobj.group)
            userid = user.id
            profile = models.Profile(country=country, mobile=mobile, role_id=roleobj.id, user_id=userid)
            profile.save()
            return http.HttpResponseRedirect(reverse('login'))
        else:
            return render(request, self.template_name, {'form': form, 'sub_form': sub_form})


@permission_required('core.view_student')
def student(request):
    return render(request, 'student.html') 

@permission_required('core.view_admin')
def admin_page(request):
    return render(request, 'admin.html') 

@permission_required('core.view_staff')
def staff_page(request):
    return render(request, 'staff.html') 

@permission_required('core.view_editor')
def editor_page(request):
    return render(request, 'editor.html') 