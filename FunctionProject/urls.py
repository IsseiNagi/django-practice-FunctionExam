from django.contrib import admin
from django.urls import path, include
from FunctionApp.views import show_error_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FunctionApp.urls')),
    path('boards/', include('boards.urls')),
]

handler404 = show_error_page
