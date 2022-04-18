from audioop import reverse
from base64 import urlsafe_b64decode

import email
from email.mime import image
from lib2to3.pgen2 import token
from multiprocessing import AuthenticationError
from urllib import request
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import Admin_Disputes, Admin_Sliders, Admin_tickets, User, Vendor_subs,Admin_Coupon
from random import randint
from ast import ExceptHandler, Try
from django.conf import settings

from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

class OtpSerailizer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(required=False)

    def validate(self, attrs):
        email = attrs.get("email")
        reset = self.context.get('reset')
        if reset :
                User.objects.get(email=email)
           
        def random_with_N_digits(n):
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)
        otp = random_with_N_digits(6)

        subject = 'Please Confirm Your Account'
        message = 'Your 6 Digit Verification Pin: {}'.format(otp)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        # send_mail(subject, message, email_from, recipient_list) 
        
        
        email = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)
        email.send()
        attrs['otp'] = otp

        
        return super().validate(attrs)
        
            


class UserSerialzer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = User
        # fields = '__all__'
        write_only_fields = ('password', )
        exclude = ('date_joined','last_login','groups','is_active','is_superuser','is_staff','user_permissions','store_name','address1','address2','country_vendor','Country_cus','state','city_town','postcode_zip','Store_Phone','Direct_Number','Website_address','Company_Incorporation','FSSAI_License','GST_Number','Recall_Plan','permissions','City','Zip','Address','Fax')

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            from django.contrib.auth.hashers import make_password
            validated_data["password"] = make_password(
                validated_data["password"])
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if  User.objects.filter(email__iexact=validated_data['email']).exists():
            raise ValidationError("Email exist with this email")
        user = super().create(validated_data)
        if validated_data['password']:
            user.set_password(validated_data['password'])
        user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(label=_("password"),
                                     style={'input_type': 'password'},
                                     trim_whitespace=False,
                                     write_only=True)
    user_type = serializers.CharField(label=_("user_type"), write_only=True)
    

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user_type=attrs.get("user_type")

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email,
                                password=password, user_type=user_type)

            if not user:
                msg = _('Invalid Credentials')
                raise serializers.ValidationError(msg, code='authentication')
            if user.user_type!=user_type:
                msg = _('User does not have permissions')
                raise serializers.ValidationError(msg, code='authentication')

        else:
            msg = _('Must include both "email" and "Password"')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

class Vendor_subs_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_subs
        fields = "__all__"

class Coupon_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Coupon
        fields = "__all__"
    
class VendorlistSerialzer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        # fields = '__all__'
        write_only_fields = ('password', )
        exclude = ('date_joined','last_login','groups','is_active','is_superuser','is_staff','user_permissions','Fax','City','Zip','Address','Country_cus')




    
class CustomerlistSerialzer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = User
        # fields = '__all__'
        write_only_fields = ('password', )
        exclude = ('date_joined','last_login','groups','is_active','is_superuser','is_staff','user_permissions','store_name','address1','address2','state','country_vendor','city_town','postcode_zip','Store_Phone','Direct_Number','Website_address','Company_Incorporation','FSSAI_License','GST_Number','Recall_Plan','user_type')



class Admin_tickets_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_tickets
        fields = "__all__"

class Admin_disputes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Disputes
        fields = "__all__"
    
class Admin_Slider_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Sliders
        fields = "__all__"

class ResetPasswordEmailRequestSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(min_length=2)
    
    class Meta:
        model=User
        fields=['email']

           
class SetNewPasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(min_length=2)
    token=serializers.CharField(min_length=1)
    uidb64=serializers.CharField(min_length=1)

    class Meta:
        model=User
        fields=['password','token','uidb64']
    def validate(self,attrs):

        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')

            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)


            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationError('the link is invalid',401)

            user.set_password(password)
            user.save()
            return (user)    
        except Exception as e:
            raise AuthenticationError('the link is invalid',401)
        return super().validate(attrs)