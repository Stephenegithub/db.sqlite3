from django.shortcuts import render, redirect

import stripe

from finance.models import Payment

stripe.api_key = "your_secret_key"


def make_payment(order_id, amount):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source="tok_visa",  # obtained with Stripe.js
            description="Payment for order #{}".format(order_id)
        )
        if charge['status'] == 'succeeded':
            # save payment information to database
            Payment.objects.create(order_id=order_id, amount=amount, status='succeeded')
            return True
        else:
            return False
    except Exception as e:
        return False


def checkout(request):
    if request.method == 'POST':
        # retrieve order information from the form
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        if make_payment(order_id, amount):
            return redirect('success')
        else:
            return redirect('failure')
    return render(request, 'checkout.html')


def success(request):
    return render(request, 'success.html')


def failure(request):
    return render(request, 'failure.html')


# views.py
from django.shortcuts import render


def create_invoice(request):
    if request.method == 'POST':
        invoice_number = request.POST.get('invoice-number')
        customer_name = request.POST.get('customer-name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        total_amount = request.POST.get('total-amount')
        payment_method = request.POST.get('payment-method')

        # Save the invoice details or perform further processing as needed
        # You can create an Invoice object and save it to the database

        # Assuming you have a model named "Invoice" defined in your models.py
        # from .models import Invoice
        # invoice = Invoice(
        #     invoice_number=invoice_number,
        #     customer_name=customer_name,
        #     email=email,
        #     address=address,
        #     total_amount=total_amount,
        #     payment_method=payment_method
        # )
        # invoice.save()

        # Redirect or display a success message
        return render(request, 'invoice_success.html')

    # Render the invoice form template for GET requests
    return render(request, 'invoice_form.html')
