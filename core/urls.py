from django.urls import include, path
from . import views
from django.contrib import admin
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("admin/", admin.site.urls),
    path("base/", views.BASE, name='base'),
    # path("users/create/", views.UserCreateView.as_view(), name='user_create'),
    path("", views.UserCreateView.as_view(), name='user_create'),
    path("student/",views.student,name='student_view'),
    path("admin_page/",views.admin_page,name='admin_view'),
    path("staff_page/",views.staff_page,name='staff_view'),
    path("editor_page/",views.editor_page,name='editor_view'),
]
