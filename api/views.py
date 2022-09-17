from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from django.conf import settings
from .models import Item, Order
from .serializers import OrderSerializer
from django.views.decorators.csrf import csrf_exempt
import stripe
import requests

def get_prices_stripe(queryset):
        items = []

        for item in queryset.items.all():
            created, stripe_price = item.create_or_update_stripe()
            print(f'Created: {created}')
            items.append({"price":stripe_price,"quantity":1})
        return items

class BuyApiView(APIView):
    """
    View for getting session with up-to-date prices by given order id.
    """
    def get(self, request, *args, **kwargs):
        try:
            order_id = kwargs['id']
        except KeyError:
            return Response({'id':'This parameter is required'})
        try:
            queryset = Order.objects.get(id=order_id)
        except Exception as e:
            return HttpResponseNotFound("Item not found")
        
        items = get_prices_stripe(queryset)

        domain_url = request.build_absolute_uri('/')[:-1]

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + f'/order/{order_id}',
                mode='payment',
                line_items=items,
                customer_email='test+location_US@example.com',
            )

            return Response({'sessionId': checkout_session['id']})
        except stripe.error.InvalidRequestError as e:
            items = get_prices_stripe(queryset)
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + f'order/{order_id}',
                mode='payment',
                line_items=items,
                customer_email='test+location_US@example.com',
            )
            return Response({'sessionId': checkout_session['id']})
        except Exception as e:
            return Response({'error': str(e)})

class OrderView(TemplateView):
    template_name = "item.html"
    
    def get(self, request, *args, **kwargs):
        try:
            pk=kwargs['id']
        except KeyError:
            return Response({'id':'This parameter is required'})
        try:
            order = Order.objects.get(id=pk)
        except:
            return HttpResponseNotFound("Item not found")
        try:
            context = {"order":order.items.all(), 'key':settings.STRIPE_PUBLISH_KEY, 'id':pk}

            return render(request, self.template_name, context)
        except Exception as e:
            print(e)

class SuccessView(TemplateView):
    template_name = "success_page.html"
    
    def get(self, request, *args, **kwargs):
        try:
            success_session = request.GET.get('session_id')
            success_session = stripe.checkout.Session.retrieve(success_session)
        except:
            return HttpResponseNotFound("Session not found")
        
        return render(request, self.template_name)