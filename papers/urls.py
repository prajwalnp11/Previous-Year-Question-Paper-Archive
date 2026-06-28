from django.urls import path
from . import views

urlpatterns = [
    path('', views.paper_list, name='paper_list'),
    path('upload/', views.paper_upload, name='paper_upload'),
    path('download/<int:pk>/', views.paper_detail, name='paper_detail'),
    
    # Subject Notes Routes
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/upload/', views.notes_upload, name='notes_upload'),
    path('notes/download/<int:pk>/', views.notes_detail, name='notes_detail'),

    # Legal and Info Compliance Routes
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact_us'),
]
