from django.urls import path

from . import views

urlpatterns = [
    path('buy/<int:id>', views.BuyApiView.as_view()),
    path('order/<int:id>', views.OrderView.as_view(),),
    path('success', views.SuccessView.as_view())
]
