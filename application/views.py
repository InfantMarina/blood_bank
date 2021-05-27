from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import os
import requests
from application.models import Donor, DonorTransaction
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def loginview(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'application/login.html')
        return HttpResponseRedirect('donor_transaction/')
    else:
        user_exist = User.objects.filter(username=request.POST['username'])
        if user_exist:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user=user)
                return HttpResponseRedirect('donor_transaction/')
            else:
                data = {'message':'Incorrect Username or Password'}
                return render(request, 'application/login.html',{'data':data})        
            
def logoutview(request):
    logout(request)
    return HttpResponseRedirect('login/')

def donors_list(request):
    donors = Donor.objects.all()
    return render(request, 'application/donors.html', {'data':donors})

def search_donor(request):
    if request.method == 'GET':
        return render(request, 'application/search_donor.html')
    else:
        search_text = request.POST['search_donor_name']
        search_location = request.POST['search_location']
        donors = Donor.objects.filter(donor_name__icontains = search_text, location__icontains = search_location)
        return render(request, 'application/donors.html', {'data':donors})

def donor_detail(request):
    if request.method == 'GET':
        data = {}
        donor_id = request.GET['donor_id']
        try:
            donor = Donor.objects.get(id=donor_id)
            data['status'] = 'success'
            data['donor'] = donor
        except Exception as e:
            if 'query does not exist' in str(e):
                data['status'] = 'failure'
                data['donor'] = None
        return render(request, 'application/donor_detail.html', {'data':data})

def update_donor(request):
    data = {}
    if request.method == 'GET':
        donor_id = request.GET['donor_id']
        try:
            donor_data = Donor.objects.get(id=donor_id)
            data['status'] = 'success'
            data['donor'] = donor_data
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = "No Donor information available for requestd donor"
            data['donor'] = None
        return render(request, 'application/update_donor.html', {'data': data})
    else:
        try:
            donor_obj = Donor.objects.get(id=request.POST['donor_id'])
            donor_obj.donor_name = request.POST['donor_name']
            donor_obj.location = request.POST['location']
            donor_obj.mobile = request.POST['mobile_no']
            donor_obj.blood_group = request.POST['blood_group']
            donor_obj.save()
            data['status'] = 'success'
            data['message'] = 'Data Updated Successfully'
            data['donor'] = donor_obj
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = 'Data Updation failed. Exception: {}'.format(str(e))
            data['donor'] = None
        return render(request, 'application/update_donor.html', {'data': data})

def add_donor(request):
    if request.method == 'GET':
        return render(request, template_name='application/add_donor.html')
    else:
        try:
            data = {}
            donor_obj = Donor()
            donor_obj.donor_name = request.POST['donor_name']
            donor_obj.location = request.POST['location']
            donor_obj.mobile = request.POST['mobile_no']
            donor_obj.blood_group = request.POST['blood_group']
            donor_obj.save()
            data['status'] = 'success'
            data['message'] = f"Donor information has been stored successfully for {request.POST['donor_name']}"
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = str(e)
        finally:
            return render(request, 'application/add_donor.html', {'data': data})


class DonorTrans(View):

    def get(self, request, transaction_id=None):
        data = {}
        if transaction_id:
            obj = DonorTransaction.objects.get(id=transaction_id)
            obj.transaction_date = datetime.strftime(obj.transaction_date,'%d-%m-%Y')
            data['transaction'] = obj
        elif 'deletion_id' in request.GET.keys():
            try:
                deletion_id = DonorTransaction.objects.get(id=request.GET['deletion_id'])
                deletion_id.delete()
                data['status'] = 'success'
                data['message'] = f'{deletion_id.donor.donor_name} has been deleted'
                data['deletion'] = deletion_id
            except Exception as e:
                data['status'] = 'failure'
                data['message'] = f'Deletion Failed. Exception: {str(e)}'
                data['deletion'] = None
        data['donors'] = Donor.objects.all()
        data['donor_transaction'] = DonorTransaction.objects.all()
        return render(request, 'application/donor_transaction/add_transaction.html', {'data':data})

    def post(self, request, transaction_id=None):
        try:
            data = {}
            if transaction_id:
                update_data = DonorTransaction.objects.get(id=transaction_id)
                update_data.transaction_date = datetime.strptime(request.POST['donated_date'],'%d-%m-%Y')
                update_data.donated_to = request.POST['donated_to']             
                update_data.receiver_mobile  = request.POST['receiver_mobile']              
                update_data.save()        
                data['status'] = 'success'
                data['message'] = f'Transaction updated successfully for {update_data.donor.donor_name}'
                data['transaction'] = update_data
            else:
                donor_obj = DonorTransaction()
                donor_obj.donor = Donor.objects.get(id=int(request.POST['select_donor']))
                donor_obj.transaction_date = datetime.strptime(request.POST['donated_date'],'%d-%m-%Y')
                donor_obj.donated_to = request.POST['donated_to']
                donor_obj.receiver_mobile  = request.POST['receiver_mobile']
                donor_obj.save()
                data['status'] = 'success'
                data['message'] = f'Transaction data has been successfully added to {donor_obj.donor.donor_name}'
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = f'Transaction failed. Exception: {str(e)}'
        return render(request, 'application/donor_transaction/add_transaction.html',{'data':data})
