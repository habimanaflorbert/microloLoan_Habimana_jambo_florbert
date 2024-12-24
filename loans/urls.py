# django imports
from django.urls import path, include
# 3rd party imports
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView)

from loans.views import LoanViewset, update_loan


route = routers.DefaultRouter()
route.register('loan', LoanViewset)

urlpatterns = [
    path('', include(route.urls)),
    path('updated/loan/<uuid:id>/', update_loan, name='updated_status'),

]