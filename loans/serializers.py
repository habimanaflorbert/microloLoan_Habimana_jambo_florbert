

from accounts.models import User
from loans.models import Loan
from rest_framework import serializers

class LoanSerializer(serializers.ModelSerializer):
    user= serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model=Loan
        fields=(
            'id',
            'user',
            'amount',
            'monthly_income',
            'status',
            'created_at'
        )
        
class LoanStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Loan.STATUS_TYPE)
