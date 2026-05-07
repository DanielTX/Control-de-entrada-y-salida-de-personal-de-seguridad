from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Registros
    path('entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('salida/', views.registrar_salida, name='registrar_salida'),

    # Consulta y reportes
    path('consulta/', views.consulta_registros, name='consulta_registros'),
    path('reporte/', views.reporte_movimientos, name='reporte_movimientos'),

    # Gestión de personal
    path('personal/', views.lista_personal, name='lista_personal'),
    path('personal/nuevo/', views.crear_personal, name='crear_personal'),

    # Gestión de áreas
    path('areas/', views.lista_areas, name='lista_areas'),
    path('areas/nueva/', views.crear_area, name='crear_area'),
]
