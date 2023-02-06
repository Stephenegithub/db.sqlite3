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
