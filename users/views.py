from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.hashers import make_password

from .models import User, CustomerProfile
from .form import RegistrationForm
from django.views import View


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm()
    template_name = 'users/register.html'

    def get(self, request):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class
        args = {}
        # username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
        # password = make_password(request.POST.get('password'))
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = make_password(request.POST.get('password'))
            print("valid")
            user = User.objects.create(username=username, password=password, email=email, customer=True)
            user.save()
            customer = CustomerProfile.objects.get(user=user)
            print(customer)
            customer.email = email
            customer.phone = request.POST.get('phone')
            customer.address = request.POST.get('address')
            customer.save()
            print("saved")
            # login(self.request, user)
            return HttpResponse("Registration Successfull!")
        else:

            args['form'] = form
            # print(args['form'])
            context = {'form': form}
            print("not valid")
            return render(request, "users/register.html", context, args)



from django_otp.oath import TOTP
from django_otp.util import random_hex
from unittest import mock
import time


class TOTPVerification(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        # customers = CustomerProfile.objects.all()
        # users = User.objects.all()
        return render(request, self.template_name)


    def __init__(self):
        # secret key that will be used to generate a token,
        # User can provide a custom value to the key.
        self.key = random_hex(20)
        # counter with which last token was verified.
        # Next token must be generated at a higher counter value.
        self.last_verified_counter = -1
        # this value will return True, if a token has been successfully
        # verified.
        self.verified = False
        # number of digits in a token. Default is 6
        self.number_of_digits = 6
        # validity period of a token. Default is 30 second.
        self.token_validity_period = 35

        print("---------------------------init--------------------")
        print(self.key)
        print(self.last_verified_counter)
        print(self.verified)
        print(self.number_of_digits)
        print(self.token_validity_period)
        print("---------------------------init--------------------")


    def totp_obj(self):
        # create a TOTP object
        print("---------------------------totp_obj-------------------")
        totp = TOTP(key=self.key,
                    step=self.token_validity_period,
                    digits=self.number_of_digits)

        # the current time will be used to generate a counter
        totp.time = time.time()
        print("---------------------------totp_obj-------------------")
        return totp

    def generate_token(self):
        print("---------------------------generate_token-------------------")
        # get the TOTP object and use that to create token
        totp = self.totp_obj()

        print(totp)
        # token can be obtained with `totp.token()`
        print(totp.token)
        token = str(totp.token).zfill(6)
        # print(str(totp.token()).zfill(6))

        print("---------------------------generate_token-------------------")
        return token

    def verify_token(self, token, tolerance=0):
        print("---------------------------verify_token-------------------")
        try:
            # convert the input token to integer
            token = int(token)
        except ValueError:
            # return False, if token could not be converted to an integer
            self.verified = False
        else:
            totp = self.totp_obj()
            # check if the current counter value is higher than the value of
            # last verified counter and check if entered token is correct by
            # calling totp.verify_token()
            if ((totp.t() > self.last_verified_counter) and
                    (totp.verify(token, tolerance=tolerance))):
                # if the condition is true, set the last verified counter value
                # to current counter value, and return True
                self.last_verified_counter = totp.t()
                self.verified = True
            else:
                # if the token entered was invalid or if the counter value
                # was less than last verified counter, then return False
                self.verified = False
        return self.verified

    def post(self, request, *args, **kwargs):
        totp = self.generate_token()
        print(totp)
        # print(totp.key)
        # print(totp.step)
        # print(totp.digits)

        # print(str(totp.token()))
        return HttpResponse("Submitted!")



if __name__ == '__main__':
    # verify token the normal way
    phone1 = token_verification()
    generated_token = phone1.generate_token()
    print("Generated token is: ", generated_token)
    token = int(input("Enter token: "))
    print(phone1.verify_token(token))
    # verify token by passing along the token validity period.
    with mock.patch('time.time', return_value=1497657600):
        print("Current Time is: ", time.time())
        generated_token = phone1.generate_token()
        print(generated_token)
    with mock.patch(
        'time.time',
            return_value=1497657600 + phone1.token_validity_period):
        print("Checking time after the token validity period has passed."
              " Current Time is: ", time.time())
        token = int(input("Enter token: "))
        print(phone1.verify_token(token, tolerance=1))