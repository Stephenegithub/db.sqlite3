from django.contrib import messages
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.models import *
from inventory.models import Product, Cart
from products.models import Product
from shipping.models import Shipping
from supply.models import SupplyTender
from .forms import *
from .forms import SignUpForm
from .models import CustomUser


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'home/home.html', context)


def reset(request):
    return render(request, 'reset.html')


def calendar(request):
    return render(request, 'calendar.html')


def customer(request):
    return render(request, 'customer/products.html')


def icons(request):
    return render(request, 'icons.html')


def profile(request):
    return render(request, 'profile.html')


# Create your views here.


@login_required
def about_us(request):
    return render(request, 'aboutus/about_us_customer.html')


@login_required
def about_s(request):
    return render(request, 'aboutus/about_us_supplier.html')


@login_required
def about_f(request):
    return render(request, 'aboutus/about_us_finance.html')


@login_required
def about_sp(request):
    return render(request, 'aboutus/about_us_dispatch.html')


@login_required
def about_i(request):
    return render(request, 'aboutus/about_us_inventory.html')


@login_required
def about_d(request):
    return render(request, 'aboutus/about_us_driver.html')


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:customer')


def user_login(request):
    loginform = LoginForm(request.POST or None)
    msg = ''

    if request.method == 'POST':
        if loginform.is_valid():
            username = loginform.cleaned_data.get('username')
            password = loginform.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.user_type == "FM":
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('accounts:finance')

                elif user.user_type == "DR":
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('accounts:driver')

                elif user.user_type == "PC":
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('accounts:designer')

                elif user.user_type == "DM":
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('accounts:dispatch')

                elif user.user_type == "Iv":
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('accounts:installer')

                elif user is not None and user.user_type == "CM":
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'You have been logged in successfully.')
                        return redirect('inventory:product-view')
                    else:
                        msg = 'Your account has not been activated. please wait for approval'

                elif user.user_type == "SP":
                    login(request, user)
                    messages.success(request, 'You have been logged in successfully.')
                    return redirect('accounts:supplier')
                else:
                    msg = 'Invalid login credentials'
            else:
                msg = 'Invalid login credentials'
        else:
            msg = 'Error validating form'

    return render(request, 'login.html', {'form': loginform, 'msg': msg})


class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "You've logged out successfully.")
        return redirect('accounts:login')


def driver(request):
    user = request.user
    if user.is_authenticated and user.user_type == CustomUser.UserTypes.DRIVER:
        pending_count = Shipping.objects.filter(driver=CustomUser, status=Shipping.Status.PENDING).count()
        delivered_count = Shipping.objects.filter(driver=CustomUser, status=Shipping.Status.DELIVERED).count()
        return render(request, 'driver/index.html',
                      {'pending_count': pending_count, 'delivered_count': delivered_count})
    else:
        return redirect(reverse_lazy('accounts:login'))


# @required_access(login_url=reverse_lazy('accounts:login'), user_type="FM")
# def finance(request):
#     # Count of approved payments
#     approved_orders = Cart.objects.filter(is_completed=True, payment__payment_status='Approved')
#     approved_payment_count = approved_orders.count()
#
#     # Count of pending payments
#     pending_orders = Cart.objects.filter(is_completed=True).exclude(payment__payment_status='Approved')
#     pending_payment_count = pending_orders.count()


# Count of paid tenders
# paid_tenders_count = SupplyTender.objects.filter(tender_status='Paid').count()
#
# context = {
#     'approved_payment_count': approved_payment_count or 0,
#     'pending_payment_count': pending_payment_count or 0,
#     'confirmed_tenders_count': confirmed_tenders_count or 0,
#     'paid_tenders_count': paid_tenders_count or 0,
# }
# return render(request, 'finance/index.html', context)


# @required_access(login_url=reverse_lazy('accounts:login'), user_type="SVP")
# def service_provider(request):
#     pending_count = Cart.objects.filter(is_completed=True).exclude(
#         Q(shipping__status='delivered') | Q(shipping__isnull=False)).count()
#     delivered_count = Cart.objects.filter(is_completed=True, shipping__status='delivered').count()
#     return render(request, 'designer/index.html', {'count': pending_count, 'delivered_count': delivered_count})


# @required_access(login_url=reverse_lazy('accounts:login'), user_type="CM")
# def customer(request):
#     user = request.user
#
#     pending_carts = Cart.objects.filter(payment__payment_status='Pending', user=user).count()
#     completed_carts = Cart.objects.filter(payment__payment_status='Approved', user=user).count()
#
#     context = {
#         'pending_carts': pending_carts,
#         'completed_carts': completed_carts,
#     }
#     return render(request, 'customer/index.html', context)


@login_required(login_url=reverse_lazy('accounts:login'))
def supplier(request):
    user = request.user
    all_tenders_count = SupplyTender.objects.filter(user=user).count()
    pending_tenders_count = SupplyTender.objects.filter(tender_status='Pending', user=user).count()
    complete_tenders_count = SupplyTender.objects.filter(tender_status='Complete', user=user).count()
    context = {
        'all_tenders_count': all_tenders_count,
        'pending_tenders_count': pending_tenders_count,
        'complete_tenders_count': complete_tenders_count,
    }
    return render(request, 'supplier/index.html', context=context)


@login_required(login_url=reverse_lazy('accounts:login'))
def dispatch(request):
    pending_count = Cart.objects.filter(is_completed=True).exclude(
        Q(shipping__status='delivered') | Q(shipping__isnull=False)).count()
    delivered_count = Cart.objects.filter(is_completed=True, shipping__status='delivered').count()
    return render(request, 'dispatch/index.html', {'count': pending_count, 'delivered_count': delivered_count})


# profiles

def customer_profile(request):
    customer_profile = CustomerProfile.objects.get(user=request.user)
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    p_form = CustomerProfileForm(instance=customer_profile)
    form = CustomerForm(instance=request.user)

    # Retrieve profile image URL

    if request.method == "POST":
        p_form = CustomerProfileForm(request.POST, request.FILES, instance=customer_profile)
        form = CustomerForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'customer_profile': customer_profile,
    }
    return render(request, 'accounts/profiles/customer-profile.html', context)


def finance_profile(request):
    finance_profile = FinanceProfile.objects.get(user=request.user)
    p_form = FinanceProfileForm(instance=finance_profile)
    form = FinanceForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = finance_profile.image.url if finance_profile.image else None

    if request.method == "POST":
        p_form = FinanceProfileForm(request.POST, request.FILES, instance=finance_profile)
        form = FinanceForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'finance_profile': finance_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/finance-profile.html', context)


def inventory_profile(request):
    inventory_profile = InventoryProfile.objects.get(user=request.user)
    p_form = InventoryProfileForm(instance=inventory_profile)
    form = InventoryForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = inventory_profile.image.url if inventory_profile.image else None

    if request.method == "POST":
        p_form = InventoryProfileForm(request.POST, request.FILES, instance=inventory_profile)
        form = InventoryForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            # Update profile image URL after saving
            profile_image_url = inventory_profile.image.url if inventory_profile.image else None
    context = {
        'p_form': p_form,
        'form': form,
        'inventory_profile': inventory_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/inventory-profile.html', context)


def driver_profile(request):
    driver_profile = DriverProfile.objects.get(user=request.user)
    p_form = DriverProfileForm(instance=driver_profile)
    form = DriverForm(instance=request.user)

    # Retrieve profile image URL

    if request.method == "POST":
        p_form = DriverProfileForm(request.POST, request.FILES, instance=driver_profile)
        form = DriverForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'driver_profile': driver_profile,

    }
    return render(request, 'accounts/profiles/driver-profile.html', context)


def supplier_profile_view(request):
    supplier_profile = SupplyProfile.objects.get(user=request.user)

    p_form = SupplierProfileForm(instance=supplier_profile)
    form = SupplierForm(instance=request.user)

    # Retrieve profile image URL

    if request.method == "POST":
        p_form = SupplierProfileForm(request.POST, request.FILES, instance=supplier_profile)
        form = SupplierForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'supplier_profile': supplier_profile
    }

    return render(request, 'accounts/profiles/supplier-profile.html', context)


# def dispatch_profile(request):
#     dispatch_profile = DispatchProfile.objects.get(user=request.user)
#
#     p_form = DispatchForm(instance=dispatch_profile)
#     form = DispatchForm(instance=request.user)
#
#     # Retrieve profile image URL
#
#     if request.method == "POST":
#         p_form = DispatchProfileForm(request.POST, request.FILES, instance=dispatch_profile)
#         form = DispatchForm(request.POST, instance=request.user)
#         if p_form.is_valid() and form.is_valid():
#             p_form.save()
#             form.save()
#             messages.success(request, 'Profile has been updated successfully')
#     context = {
#         'p_form': p_form,
#         'form': form,
#         'dispatch_profile': dispatch_profile,
#     }
#     return render(request, 'accounts/profiles/dispatch-profile.html', context)


def packer_profile(request):
    packer_profile = PackerProfile.objects.get(user=request.user)

    p_form = PackerProfileForm(instance=packer_profile)
    form = PackerProfileForm(instance=request.user)

    # Retrieve profile image URL

    if request.method == "POST":
        p_form = PackerProfileForm(request.POST, request.FILES, instance=packer_profile)
        form = PackerProfileForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'dispatch_profile': packer_profile,
    }
    return render(request, 'accounts/profiles/packer-profile.html', context)


def customer_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/customer-change-password.html', {'form': form})


def driver_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/driver-change-password.html', {'form': form})


def supplier_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/supplier-change-password.html', {'form': form})


def finance_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/finance-change-password.html', {'form': form})


def inventory_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/inventory-change-password.html', {'form': form})


def packer_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/packer-change-password.html', {'form': form})


def dispatch_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/diapatch-change-password.html', {'form': form})


# messages


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Message


class SendMessageView(CreateView):
    model = Message
    fields = ['name', 'email', 'subject', 'message']
    template_name = 'send_message.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # set the current user as the sender
        form.instance.sender = self.request.user
        # set the is_read field to False
        form.instance.is_read = False
        return super().form_valid(form)


from django.views.generic import ListView
from .models import FAQ


class FAQQuestionTypeListView(ListView):
    template_name = 'faq/customer_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


class D_FAQ(ListView):
    template_name = 'faq/driver_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


class S_FAQ(ListView):
    template_name = 'faq/service_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


class F_FAQ(ListView):
    template_name = 'faq/finance_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


class I_FAQ(ListView):
    template_name = 'faq/inventory_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


class SP_FAQ(ListView):
    template_name = 'faq/supplier_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


# feedback module

from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Conversation, Message


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messages/conversation_list.html'
    context_object_name = 'conversations'
    login_url = 'login'

    def get_queryset(self):
        # Get conversations where the logged in user is either user1 or user2
        return Conversation.objects.filter(models.Q(user1=self.request.user) | models.Q(user2=self.request.user))


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messages/conversation_detail.html'
    context_object_name = 'conversation'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        context['messages'] = conversation.messages.all()
        context['recipient'] = conversation.user1 if conversation.user1 != self.request.user else conversation.user2
        return context


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        sender = request.user
        recipient = conversation.user1 if conversation.user2 == sender else conversation.user2
        content = request.POST.get('content')
        message = Message.objects.create(conversation=conversation, sender=sender, recipient=recipient, content=content)
        return HttpResponseRedirect(reverse('accounts:conversation_detail', args=[conversation.pk]))


class MarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        messages = conversation.messages.filter(recipient=request.user, read=False)
        messages.update(read=True)
        return HttpResponseRedirect(reverse('accounts:conversation_detail', args=[conversation.pk]))


# chat testing codes
class StartConversationView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(user_type=User.UserTypes.FINANCE).exclude(
            id=request.user.id)  # filter finance users and exclude the logged in user
        return render(request, 'messages/start_conversation.html', {'users': users})

    def post(self, request):
        recipient_id = request.POST.get('recipient')
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.objects.create(user1=request.user, user2=recipient)
        content = request.POST.get('message')
        message = Message.objects.create(conversation=conversation, sender=request.user, recipient=recipient,
                                         content=content)
        return HttpResponseRedirect(reverse('accounts:conversation_detail', args=[conversation.pk]))


# chat testing codes
class CustomerStartConversationView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(user_type=User.UserTypes.SERVICE_PROVIDER).exclude(
            id=request.user.id)  # filter finance users and exclude the logged in user
        return render(request, 'messages/s_start_conversation.html', {'users': users})

    def post(self, request):
        recipient_id = request.POST.get('recipient')
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.objects.create(user1=request.user, user2=recipient)
        content = request.POST.get('message')
        message = Message.objects.create(conversation=conversation, sender=request.user, recipient=recipient,
                                         content=content)
        return HttpResponseRedirect(reverse('accounts:conversation_detail', args=[conversation.pk]))


# finance

class FinanceConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messages/finance/conversation_list.html'
    context_object_name = 'conversations'
    login_url = 'login'

    def get_queryset(self):
        # Get conversations where the logged in user is either user1 or user2
        return Conversation.objects.filter(models.Q(user1=self.request.user) | models.Q(user2=self.request.user))


class FinanceConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messages/finance/conversation_detail.html'
    context_object_name = 'conversation'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        context['messages'] = conversation.messages.all()
        context['recipient'] = conversation.user1 if conversation.user1 != self.request.user else conversation.user2
        return context


class FinanceSendMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        sender = request.user
        recipient = conversation.user1 if conversation.user2 == sender else conversation.user2
        content = request.POST.get('content')
        message = Message.objects.create(conversation=conversation, sender=sender, recipient=recipient, content=content)
        return HttpResponseRedirect(reverse('accounts:Finance_conversation_detail', args=[conversation.pk]))


class FinanceMarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        messages = conversation.messages.filter(recipient=request.user, read=False)
        messages.update(read=True)
        return HttpResponseRedirect(reverse('accounts:Finance_conversation_detail', args=[conversation.pk]))


# chat testing codes
class FinanceStartConversationView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(user_type=User.UserTypes.CUSTOMER).exclude(
            id=request.user.id)  # filter finance users and exclude the logged in user
        return render(request, 'messages/finance/start_conversation.html', {'users': users})

    def post(self, request):
        recipient_id = request.POST.get('recipient')
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.objects.create(user1=request.user, user2=recipient)
        content = request.POST.get('message')
        message = Message.objects.create(conversation=conversation, sender=request.user, recipient=recipient,
                                         content=content)
        return HttpResponseRedirect(reverse('accounts:Finance_conversation_detail', args=[conversation.pk]))


# service provider

class ServiceConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'messages/service provider/conversation_list.html'
    context_object_name = 'conversations'
    login_url = 'login'

    def get_queryset(self):
        # Get conversations where the logged in user is either user1 or user2
        return Conversation.objects.filter(models.Q(user1=self.request.user) | models.Q(user2=self.request.user))


class ServiceConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'messages/service provider/conversation_detail.html'
    context_object_name = 'conversation'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        context['messages'] = conversation.messages.all()
        context['recipient'] = conversation.user1 if conversation.user1 != self.request.user else conversation.user2
        return context


class ServiceSendMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        sender = request.user
        recipient = conversation.user1 if conversation.user2 == sender else conversation.user2
        content = request.POST.get('content')
        message = Message.objects.create(conversation=conversation, sender=sender, recipient=recipient, content=content)
        return HttpResponseRedirect(reverse('accounts:service_conversation_detail', args=[conversation.pk]))


class ServiceMarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        messages = conversation.messages.filter(recipient=request.user, read=False)
        messages.update(read=True)
        return HttpResponseRedirect(reverse('accounts:service_conversation_detail', args=[conversation.pk]))


# chat testing codes
class ServiceStartConversationView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.filter(user_type=User.UserTypes.CUSTOMER).exclude(
            id=request.user.id)  # filter finance users and exclude the logged in user
        return render(request, 'messages/service provider/start_conversation.html', {'users': users})

    def post(self, request):
        recipient_id = request.POST.get('recipient')
        recipient = User.objects.get(id=recipient_id)
        conversation = Conversation.objects.create(user1=request.user, user2=recipient)
        content = request.POST.get('message')
        message = Message.objects.create(conversation=conversation, sender=request.user, recipient=recipient,
                                         content=content)
        return HttpResponseRedirect(reverse('accounts:service_conversation_detail', args=[conversation.pk]))
