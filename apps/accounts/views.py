from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import (
    RememberPasswordForm,  # ✅ نام اصلاح‌شده
    UpdateProfileForm,
    RegisterUserForm,
    VerifyRegisterForm,
    LoginUserForm,
    ChangePasswordForm
)
import utils
from .models import CustomUser, Customer
from apps.specialties.models import Expert
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from apps.orders.models import Order
from apps.payments.models import Payment
from django.contrib.auth.decorators import login_required
from apps.specialties.form import ExpertForm


# ================================================================
# ثبت‌نام کاربر
# ================================================================
class RegisterUserView(View):
    template_name = 'account_app/register.html'
    
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            # دریافت فیلدها
            mobile_number = data.get('mobile_number', '').strip()
            name = data.get('name', '').strip()
            family = data.get('family', '').strip()
            email = data.get('email', '').strip()
            gender = data.get('gender', True)
            password = data.get('password1', '')
            
            # اعتبارسنجی شماره موبایل
            if not mobile_number:
                messages.error(request, 'شماره موبایل الزامی است', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # بررسی وجود شماره موبایل
            if CustomUser.objects.filter(mobile_number=mobile_number).exists():
                messages.error(request, 'این شماره موبایل قبلاً ثبت شده است', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # بررسی تطابق رمز عبور
            password2 = data.get('password2', '')
            if password != password2:
                messages.error(request, 'رمز عبور و تکرار آن مطابقت ندارند', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # بررسی طول رمز عبور
            if len(password) < 8:
                messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # ایجاد کد فعال‌سازی
            active_code = utils.create_random_code(5)
            
            # ایجاد کاربر
            try:
                user = CustomUser.objects.create_user(
                    mobile_number=mobile_number,
                    email=email,
                    name=name,
                    family=family,
                    active_code=active_code,
                    gender=gender,
                    password=password,
                )
                
                # ایجاد پروفایل Customer
                Customer.objects.create(user=user)
                
                # ارسال پیامک (اختیاری - اگر خطا داد ادامه بده)
                try:
                    utils.send_sms(mobile_number, active_code)
                except:
                    pass  # اگر پیامک ارسال نشد، خطا نده
                
                
                
                # ذخیره در سشن
                request.session['user_session'] = {
                    'active_code': str(active_code),
                    'mobile_number': mobile_number,
                    'remember_password': False
                }
                
                messages.success(request, 'ثبت‌نام با موفقیت انجام شد. کد فعال‌سازی را وارد کنید', 'success')
                return redirect('accounts:verify')
                
            except Exception as e:
                messages.error(request, f'خطا در ثبت‌نام: {str(e)}', 'danger')
                return render(request, self.template_name, {'form': form})
        
        # اگر فرم معتبر نبود
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}', 'danger')
            
            messages.error(request, 'خطا در انجام ثبت‌نام. لطفاً اطلاعات را بررسی کنید', 'danger')
            return render(request, self.template_name, {'form': form})


# ================================================================
# تأیید کد فعال‌سازی
# ================================================================
class VerifyRegisterCodeView(View):
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # بررسی وجود سشن
        if 'user_session' not in request.session:
            messages.error(request, 'لطفاً ابتدا ثبت‌نام کنید', 'danger')
            return redirect('accounts:register')
        
        form = VerifyRegisterForm()
        return render(request, 'account_app/verify_regester_code.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session.get('user_session')
            
            if not user_session:
                messages.error(request, 'اطلاعات ثبت‌نام یافت نشد. لطفاً دوباره ثبت‌نام کنید', 'danger')
                return redirect('accounts:register')
            
            # بررسی کد فعال‌سازی
            if data['active_code'] == user_session.get('active_code'):
                try:
                    user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                    user.is_active = True
                    user.active_code = None  # پاک کردن کد بعد از فعال‌سازی
                    user.save()
                    
                    # پاک کردن سشن
                    del request.session['user_session']
                    
                    messages.success(request, 'حساب کاربری شما با موفقیت فعال شد. لطفاً وارد شوید', 'success')
                    return redirect('accounts:login')
                    
                except CustomUser.DoesNotExist:
                    messages.error(request, 'کاربر یافت نشد. لطفاً دوباره ثبت‌نام کنید', 'danger')
                    return redirect('accounts:register')
            
            else:
                messages.error(request, 'کد فعال‌سازی وارد شده اشتباه است', 'danger')
                return render(request, 'account_app/verify_regester_code.html', {'form': form})
        
        messages.error(request, 'لطفاً کد فعال‌سازی را به‌درستی وارد کنید', 'danger')
        return render(request, 'account_app/verify_regester_code.html', {'form': form})


# ================================================================
# ورود کاربر
# ================================================================
class loginUserView(View):
    template_name = 'account_app/login.html'
    
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            mobile_number = data['mobile_number']
            password = data['password']
            
            # احراز هویت
            user = authenticate(request, username=mobile_number, password=password)
            
            if user is not None:
                # بررسی فعال بودن کاربر
                if not user.is_active:
                    messages.error(request, 'حساب کاربری شما فعال نیست. لطفاً کد فعال‌سازی را وارد کنید', 'danger')
                    return render(request, self.template_name, {'form': form})
                
                # بررسی ادمین نبودن
                if user.is_admin:
                    messages.error(request, 'کاربر ادمین نمی‌تواند از این بخش وارد شود', 'danger')
                    return render(request, self.template_name, {'form': form})
                
                # ورود موفق
                login(request, user)
                messages.success(request, f'خوش آمدید {user.name}', 'success')
                
                # هدایت به صفحه قبلی
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('main:index')
            
            else:
                messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است', 'danger')
                return render(request, self.template_name, {'form': form})
        
        messages.error(request, 'لطفاً اطلاعات را به‌درستی وارد کنید', 'danger')
        return render(request, self.template_name, {'form': form})


# ================================================================
# خروج کاربر
# ================================================================
class LogoutUserView(View):
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # حفظ سبد خرید
        session_data = request.session.get('shop_cart')
        logout(request)
        if session_data:
            request.session['shop_cart'] = session_data
        
        messages.success(request, 'با موفقیت خارج شدید', 'success')
        return redirect('main:index')


# ================================================================
# تغییر رمز عبور
# ================================================================
class ChangePasswordView(View):
    template_name = 'account_app/change_password.html'
    
    def dispatch(self, request, *args: Any, **kwargs: Any):
        # فقط کاربرانی که لاگین هستند یا سشن دارند
        if not request.user.is_authenticated and 'user_session' not in request.session:
            messages.error(request, 'لطفاً ابتدا وارد شوید', 'danger')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            password1 = data.get('password1')
            password2 = data.get('password2')
            
            # ====== بررسی تطابق رمز ======
            if password1 != password2:
                messages.error(request, 'رمز عبور و تکرار آن مطابقت ندارند', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # ====== بررسی طول رمز ======
            if len(password1) < 8:
                messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد', 'danger')
                return render(request, self.template_name, {'form': form})
            
            # ====== دریافت کاربر ======
            user = None
            
            # 1. اگر کاربر لاگین است
            if request.user.is_authenticated:
                user = request.user
            
            # 2. اگر از طریق سشن (فراموشی رمز) آمده است
            elif 'user_session' in request.session:
                mobile_number = request.session['user_session'].get('mobile_number')
                try:
                    user = CustomUser.objects.get(mobile_number=mobile_number)
                except CustomUser.DoesNotExist:
                    messages.error(request, 'کاربر یافت نشد', 'danger')
                    return redirect('accounts:login')
            
            # 3. اگر هیچکدام
            else:
                messages.error(request, 'لطفاً ابتدا وارد شوید', 'danger')
                return redirect('accounts:login')
            
            # ====== تغییر رمز عبور ======
            try:
                user.set_password(password1)
                user.active_code = utils.create_random_code(5)
                user.save()
                
                # پاک کردن سشن اگر وجود دارد
                if 'user_session' in request.session:
                    del request.session['user_session']
                
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد. لطفاً دوباره وارد شوید', 'success')
                return redirect('accounts:login')
                
            except Exception as e:
                messages.error(request, f'خطا در تغییر رمز عبور: {str(e)}', 'danger')
                return render(request, self.template_name, {'form': form})
        
        # اگر فرم معتبر نبود
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}', 'danger')
            
            messages.error(request, 'اطلاعات وارد شده صحیح نمی‌باشد', 'danger')
            return render(request, self.template_name, {'form': form})
# ================================================================
# فراموشی رمز عبور
# ================================================================
class RememberPasswordView(View):
    template_name = 'account_app/remember_password.html'
    
    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            mobile_number = data['mobile_number']
            
            try:
                user = CustomUser.objects.get(mobile_number=mobile_number)
                active_code = utils.create_random_code(5)
                
                # ذخیره کد در دیتابیس
                user.active_code = active_code
                user.save()
                
                # ارسال پیامک (اختیاری)
                try:
                    utils.send_sms(mobile_number, f'کد تأیید شما: {active_code}')
                except:
                    pass
                
                    
                
                # ذخیره در سشن
                request.session['user_session'] = {
                    'active_code': str(active_code),
                    'mobile_number': mobile_number,
                    'remember_password': True,
                }
                
                messages.success(request, 'کد تأیید به شماره موبایل شما ارسال شد', 'success')
                return redirect('accounts:verify')
                
            except CustomUser.DoesNotExist:
                messages.error(request, 'این شماره موبایل در سیستم ثبت نشده است', 'danger')
                return render(request, self.template_name, {'form': form})
        
        messages.error(request, 'لطفاً شماره موبایل را به‌درستی وارد کنید', 'danger')
        return render(request, self.template_name, {'form': form})


# ================================================================
# پنل کاربری
# ================================================================
class UserPanelView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "phone_number": customer.phone_number,
                "address": customer.address,
                "image": customer.image_name,
                "mobile_number": user.mobile_number,
            }
        except ObjectDoesNotExist:
            user_info = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "mobile_number": user.mobile_number,
            }
        
        return render(request, 'account_app/userpanel.html', {"user_info": user_info})


# ================================================================
# پنل کاربری متخصص
# ================================================================
class UserPaneExpertlView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        experts = Expert.objects.filter(is_active=True)
        
        user_info = {
            "name": user.name,
            "family": user.family,
            "email": user.email,
            "mobile_number": user.mobile_number,
        }
        
        return render(request, 'account_app/userpanel_expert.html', {
            "user_info": user_info,
            "experts": experts
        })


# ================================================================
# ویرایش پروفایل (کامل با تصویر)
# ================================================================
class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        # اطلاعات اولیه
        initial_dict = {
            "mobile_number": user.mobile_number,
            "name": user.name,
            "family": user.family,
            "email": user.email,
        }
        
        # اطلاعات از Customer
        try:
            customer = Customer.objects.get(user=user)
            initial_dict.update({
                "phone_number": customer.phone_number,
                "address": customer.address,
            })
        except ObjectDoesNotExist:
            pass
        
        form = UpdateProfileForm(initial=initial_dict)
        return render(request, 'account_app/update_profile.html', {"form": form})
    
    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            
            # به‌روزرسانی اطلاعات کاربر
            user.name = cd['name']
            user.family = cd['family']
            user.email = cd['email']
            user.save()
            
            # به‌روزرسانی یا ایجاد Customer
            try:
                customer = Customer.objects.get(user=user)
                customer.phone_number = cd.get('phone_number', '')
                customer.address = cd.get('address', '')
                if 'image' in request.FILES:
                    customer.image_name = cd['image']
                customer.save()
            except ObjectDoesNotExist:
                customer = Customer.objects.create(
                    user=user,
                    phone_number=cd.get('phone_number', ''),
                    address=cd.get('address', ''),
                    image_name=cd.get('image', None),
                )
            
            messages.success(request, 'پروفایل با موفقیت ویرایش شد', 'success')
            return redirect('accounts:userpanel')
        
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمی‌باشد', 'danger')
            return render(request, 'account_app/update_profile.html', {'form': form})


# ================================================================
# نمایش آخرین سفارشات
# ================================================================
@login_required
def show_last_orders(request):
    orders = Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:4]
    return render(request, 'account_app/partials/show_last_orders.html', {'orders': orders})


# ================================================================
# نمایش پرداخت‌های کاربر
# ================================================================
@login_required
def show_user_payments(request):
    orders = Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:4]
    return render(request, 'account_app/partials/show_last_orders.html', {'orders': orders})