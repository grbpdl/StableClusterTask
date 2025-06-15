from django.urls import path
from .views import ContactMessageView

urlpatterns = [
    path('api/contact/', ContactMessageView.as_view(), name='contact'),
]