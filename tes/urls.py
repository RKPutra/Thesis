from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('hasil/', views.hasil, name='hasil'),
    path('single/', views.single, name='single'),
    path('login/', views.login, name='login'),
    path('cekLogin/', views.cekLogin, name='cekLogin'),
    path('logout/', views.logout, name='logout'),
    path('tambah_dokter/', views.tambahDokter, name='tambahDokter'),
    path('prosesTambahDokter/', views.prosesTambahDokter, name='prosesTambahDokter'),
    path('ganti_parameter/', views.gantiParameter, name='gantiParameter'),
    path('prosesGantiParameter/', views.prosesGantiParameter, name='prosesGantiParameter'),
    path('training/', views.training, name='training'),
    path('hasilTraining/', views.hasilTraining, name='hasilTraining'),
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('hasilDiagnosis/', views.hasilDiagnosis, name='hasilDiagnosis'),
]