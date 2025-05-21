from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from .forms import SignUpForm, LoginForm, PhoneForm, OTPForm
from .models import CustomUser
import random
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import login
from kavenegar import KavenegarAPI, APIException
from django.utils.crypto import get_random_string



class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('accounts:login')


class PhoneSignupView(View):
    form_class = PhoneForm
    template_name = 'accounts/phone_signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            # Check if phone number already exists
            if CustomUser.objects.filter(phone_number=phone).exists():
                messages.error(request, 'این شماره تلفن قبلا ثبت شده است')
                return render(request, self.template_name, {'form': form})

            # Store phone number and registration flag in session
            request.session['phone_for_otp'] = phone
            request.session['is_registration'] = True

            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            cache.set(f'otp_{phone}', otp, timeout=300)  # 5 minutes expiry

            # Send OTP via Kavenegar
            try:
                api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
                # Using lookup instead of sms_send
                params = {
                    'receptor': phone,
                    'token': otp,
                    'template': 'verify'  # Use your template name here
                }
                response = api.verify_lookup(params)
                messages.success(request, 'کد تایید به شماره شما ارسال شد')
                return redirect('accounts:verify_otp')
            except APIException as e:
                messages.error(request, f'خطا در ارسال کد تایید: {str(e)}')
            except Exception as e:
                messages.error(request, f'خطای سیستمی: {str(e)}')

        return render(request, self.template_name, {'form': form})


class SendOTPView(View):
    form_class = PhoneForm
    template_name = 'accounts/send_otp.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            # Check if user exists
            user_exists = CustomUser.objects.filter(phone_number=phone).exists()
            request.session['is_registration'] = not user_exists

            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Store OTP in cache with 2-minute expiration
            cache.set(f'otp_{phone}', otp, 120)

            # Store phone in session
            request.session['phone_for_otp'] = phone

            # Send OTP via Kavenegar basic Send method
            try:
                api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

                # Format the message with the OTP code
                message = f"کد تایید شما: {otp}"

                params = {
                    'sender': settings.KAVENEGAR_SENDER,  # Using the sender line from settings
                    'receptor': phone,
                    'message': message
                }

                response = api.sms_send(params)
                messages.success(request, 'کد تایید با موفقیت ارسال شد')
                return redirect('accounts:verify_otp')
            except APIException as e:
                messages.error(request, f'خطا در ارسال کد تایید: {e}')
            except Exception as e:
                messages.error(request, f'خطا در ارسال کد تایید: {e}')

        return render(request, self.template_name, {'form': form})

class VerifyOTPView(View):
    form_class = OTPForm
    template_name = 'accounts/verify_otp.html'

    def get(self, request):
        # Check if we have a phone in session
        if 'phone_for_otp' not in request.session:
            messages.error(request, 'لطفا ابتدا شماره تلفن خود را وارد کنید')
            return redirect('accounts:send_otp')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            phone = request.session.get('phone_for_otp')

            if not phone:
                messages.error(request, 'لطفا ابتدا شماره تلفن خود را وارد کنید')
                return redirect('accounts:send_otp')

            # Verify OTP
            cached_otp = cache.get(f'otp_{phone}')

            if cached_otp and otp == cached_otp:
                # OTP is correct
                is_registration = request.session.get('is_registration', False)

                try:
                    if is_registration:
                        # Create a new user
                        username = f'phone_{phone}'
                        #password = CustomUser.objects.make_random_password()
                        password = get_random_string(length=12)
                        user = CustomUser.objects.create_user(
                            username=username,
                            phone_number=phone,
                            password=password
                        )
                        messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد')
                    else:
                        # Login existing user
                        user = CustomUser.objects.get(phone_number=phone)

                    # Log in user with explicit backend
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    # Clear session data
                    if 'phone_for_otp' in request.session:
                        del request.session['phone_for_otp']
                    if 'is_registration' in request.session:
                        del request.session['is_registration']

                    # Clear OTP from cache
                    cache.delete(f'otp_{phone}')

                    messages.success(request, 'شما با موفقیت وارد شدید')
                    return redirect('/')

                except CustomUser.DoesNotExist:
                    messages.error(request, 'کاربر یافت نشد')
            else:
                messages.error(request, 'کد وارد شده صحیح نیست')

        return render(request, self.template_name, {'form': form})




