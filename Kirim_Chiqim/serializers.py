from rest_framework import serializers
from .models import Account
from .models import VIA_EMAIL, VIA_PHONE, DONE
from base.utils import input_regix
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime

class SignUpSerializer(serializers.ModelSerializer):
    email_or_phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['auth_status', 'auth_type', 'email_or_phone_number']
        read_only_fields = ['auth_status', 'auth_type']



    def validate(self, attrs):
        user_input = attrs.get('email_or_phone_number')

        user_is_exists = Account.objects.filter(Q(phone_number = user_input)| Q(email = user_input)).first()
        if user_is_exists:
            if user_is_exists.auth_status == DONE:
                raise ValidationError('Ushbu foydalanuvchi mavjud')
            else:
                self.code_checking(user_is_exists)
                user_is_exists.delete()
                


        user_input_type = input_regix(user_input)

        if user_input_type == 'via_email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }

        elif user_input_type == "via_phone":
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE
            }

        else:
            raise ValidationError('Email yoki phone_number xato kiritildi qayta kiriting!')
        
        return data
    

    def create(self, validated_data):
        user = Account(**validated_data)
        user.save()

        if user.auth_type == VIA_EMAIL:
            code = user.generate_code(user.auth_type)
            print(f'----------{code}----------')

        elif user.auth_type == VIA_PHONE:
            code = user.generate_code(user.auth_type)
            print(f'----------{code}----------')

        else:
            raise ValidationError('Email  yoki telefon raqam xato kiritilgan!')
        
        return user
    


    def code_checking(self, user):
        code = user.codes.all().filter(used = False, expired_time__gte = datetime.now()).first()
        if code:
            raise ValidationError('Sizda hali aktiv kod mavjud')




    def to_representation(self, instance):
        data = super().to_representation(instance)

        return {
            'tokens': instance.token(),
            'data': data
            
        }
    

class UPdateUserPropertiesSerializer(serializers.ModelSerializer):
    conf_password = serializers.CharField(write_only = True)
    class Meta:
        model = Account
        fields = ['username', 'password', 'conf_password']

    def validate(self, attrs):
        password = attrs.get('password')
        conf_password = attrs.get('conf_password')
        if not password or not conf_password:
            raise ValidationError('Parol kiritilishi shart!')
        
        if password != conf_password:
            raise ValidationError('Parollar mos emas!')
        
        attrs.pop('conf_password')
        
        return attrs
    
    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'data': data,
            'msg': 'Account muvaffaqiyatli yaratildi'
        }
    