from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView

from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    # path('', required_access (function=TemplateView.as_view(template_name="index.html"),
    #                          login_url=reverse_lazy('accounts:login'), user_type="CM"), name="index")

]
