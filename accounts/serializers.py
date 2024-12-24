from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from rest_framework import serializers

from accounts.models import User



class AccountCreationSerializer(serializers.ModelSerializer):

    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICE,required=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'telephone',
            'first_name',
            'last_name',
            'password',
            'user_type',
        )
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(
            user_type=validated_data.get('user_type'),first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'), telephone=validated_data.get('telephone'),  password=validated_data.get('password'))
      
        
        return user


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model=User
        fields=(
            'id',
            'first_name',
            'lasst_name',
            'telephone',
            'user_type',
        )


class UserPasswordSerializer(serializers.ModelSerializer):
    recent_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
    user= serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    def validate(self,data):
        if check_password(data.get('recent_password'), data.get('user').password):
            if data.get('new_password') != data['recent_password']:
                return data
            raise  serializers.ValidationError("Password don't match")
        raise serializers.ValidationError("Use Correct password")
    
    class Meta:
        model=User
        fields=(
            'id',
            'recent_password',
            'new_password',
            'user'
        )
    
