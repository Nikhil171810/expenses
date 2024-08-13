from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('home/', views.home, name='home'),
    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('view_expense', views.view_expense, name='view_expense'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_category/', views.add_category, name='add_category'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]                   