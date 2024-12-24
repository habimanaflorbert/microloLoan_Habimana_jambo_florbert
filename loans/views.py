from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import mixins
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,BasePermission
from accounts.models import User
from loans.models import Loan
from loans.permissions import IsAdmin, IsEndUser
from loans.serializers import LoanSerializer, LoanStatusSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN


# Create your views here.


class LoanViewset(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [BasePermission]
    queryset = Loan.objects.all()


    def get_queryset(self):
        if self.request.user.user_type==User.END_USER:
            return Loan.objects.filter(user=self.request.user)
        else:
            return Loan.objects.filter()
        
    def get_permissions(self):
        
        if self.request.method == 'POST':
            self.permission_classes = [IsEndUser]
        
        
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    
@api_view(["PATCH"])
@permission_classes((IsAdmin,))
def update_loan(request,id):
    try:
        loan=Loan.objects.get(id=id)
        serializer = LoanStatusSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        loan.status=serializer.validated_data['status']
        loan.save()
        return Response(status=HTTP_201_CREATED)
    except Loan.DoesNotExist:
        return Response(status= HTTP_403_FORBIDDEN)