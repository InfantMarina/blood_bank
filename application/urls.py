from django.contrib import admin
from django.urls import path, re_path
from application import views
from django.contrib.auth.decorators import login_required

app_name = "application"

urlpatterns = [
    re_path('^$', views.donors_list, name="home" ),
    re_path('^donors/$', views.donors_list, name="donors"),
    re_path('^add_donor/$', views.add_donor, name='add_donor'),
    re_path('^search_donor/$', views.search_donor, name='search_donor'),
    re_path('^donor_detail/$', views.donor_detail, name='donor_detail'),
    re_path('^donor_update/$', views.update_donor, name='update_donor'),
    re_path('^donor_transaction/(?P<transaction_id>[0-9]{1,4})?/?$', login_required(views.DonorTrans.as_view()), name='donor_transaction' ),
    re_path('^login/?', views.loginview, name='login'),
    re_path('^logout/?', views.logoutview, name='logout')
]
