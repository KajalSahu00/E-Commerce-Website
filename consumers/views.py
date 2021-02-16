from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomerForm, CustomerSignUpForm, CustomerLoginForm
from consumers.models import Customer, CustomerProfile
import pyotp
import base64
from datetime import datetime
from twilio.rest import Client
from consumers.utility import UNAUTHORISED, OTP_INVALID, AUTHORISED
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.contrib import messages


expiry_time = 120
# Create your views here.
def generate_key(phoneNumber):
    return str(phoneNumber) + str(datetime.date(datetime.now())) + "kjsdk787766566"

def get_otp(phoneNumber):
    key_gen = generate_key(phoneNumber)
    key = base64.b32encode(key_gen.encode())
    otp = pyotp.TOTP(key, interval=expiry_time)
    return otp.now(), key_gen

def send_otp(phoneNumber, generated_otp):
    account_sid = 'ACe62c487ed128a0556bf689001aed12ed'
    auth_token = '53ed973995f7cdf9438e1ecf00e2ea16'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = 'Your otp is' + str(generated_otp),
        from_ = '+19542105137',
        to = '+91' + str(phoneNumber)
    )
    print(message.sid)

def create_user(request):
    if request.method == 'POST':

        form = CustomerForm(request.POST or None)

        if form.is_valid():
            phoneNumber = form.cleaned_data['mobile']

            isUserExists = Customer.objects.filter(mobile=phoneNumber)
            if not isUserExists:
                form.save()

            generated_otp, key_gen = get_otp(phoneNumber)
            send_otp(phoneNumber, generated_otp)

            request.session['key_gen'] = key_gen
            request.session['mobile'] = phoneNumber
            messages.success(request, 'We have sent the otp on your mobile number.')
            messages.warning(request, 'Valid for 1 minute only.')
            return render(request, 'otp.html')
        return render(request, 'account.html', {'form': form})
    else:
        form = CustomerForm()
    messages.info(request, 'Fill out the form.')
    return render(request, 'account.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        user = get_object_or_404(Customer, mobile=request.session['mobile'])
        key_gen = request.session['key_gen']
        key = base64.b32encode(key_gen.encode())
        otp = pyotp.TOTP(key, interval=expiry_time)
        
        user_otp = request.POST.get('otp')
    
        if otp.verify(user_otp):
            user.isVerified = True
            user.save()
            messages.success(request, 'Your mobile number is Verified.')
            if user.isCreated:
                return redirect('login')
            return redirect('signup_form')
        messages.warning(request, 'Invalid Otp')
        return redirect('account')
    messages.info(request, 'Fill out the form.')
    return redirect('account')

def signup_form(request):
    if request.method == 'POST':

        form = CustomerForm(request.POST)
        profile_form = CustomerSignUpForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            customer = get_object_or_404(Customer, mobile=form.cleaned_data['mobile'])
            if not customer.isCreated and customer.isVerified:
                profile = profile_form.save(commit=False)
                profile.password = make_password(profile_form.cleaned_data['password'])
                profile.customer = customer
                profile.save()
                customer.isCreated = True
                customer.save()
                messages.success(request, 'Your account is successfully created.')
                return redirect('login')
            messages.warning(request, 'Account already exists with this mobile number or this number is not verified.')
            return redirect('account')
        return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})

    else:
        form = CustomerForm()
        profile_form = CustomerSignUpForm()
    messages.info(request, 'Fill out the form.')
    return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})

def login(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        login_form = CustomerLoginForm(request.POST)
        if form.is_valid() and login_form.is_valid():
            try:
                customer = Customer.objects.get(mobile=form.cleaned_data['mobile'])
            except ObjectDoesNotExist:
                messages.info(request, 'Customer with this mobile number does not exist.')
                return render(request, 'login.html', {'form': form, 'login_form': login_form})
            if check_password(login_form.cleaned_data['password'], customer.customerprofile.password):
                request.session['customer'] = customer.id
                messages.success(request, 'You are successfully logged in.')
                return redirect('products:index')
            messages.warning(request, "Password is incorrect.")
            return redirect('login')
    else:
        form = CustomerForm()
        login_form = CustomerLoginForm()
    return render(request, 'login.html', {'form': form, 'login_form': login_form})

def logout(request):
    request.session.clear()
    return redirect('account')