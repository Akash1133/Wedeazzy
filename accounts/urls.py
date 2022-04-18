from unicodedata import name
from django.urls import path, include
from django.urls import re_path as url
from .views import *



urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('reset-password-otp', ResetPasswordOtpView.as_view()),
    path('verify-otp', VerifyOtp.as_view()),
    path('user-detail', UserDetailView.as_view()),
    path('logout',logout_view),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckApi.as_view(),name="password-reset-confirm"),
    path('password-reset-complete/',SetNewPasswordApiView.as_view(),name="password-reset-complete"),


   
    
    # path('customer/',CustomerListView.as_view()),
    path('customer/<int:pk>',CustomerlistView.as_view()),
    path('customer/',CustomerNameView.as_view()),
    path('vendor-subscription/', Vendor_subs_List.as_view()),
    path('vendor-subscription', VendorSubsCreateView.as_view()),
    path('vendor-subscription/<int:pk>', VendorSubsView.as_view()),
    path('admin-coupon/', Admin_Coupon_List.as_view()),
    path('admin-coupon', AdminCouponCreateView.as_view()),
    path('admin-coupon/<int:pk>', AdminCouponView.as_view()),
    #path('admin-coupon1',AdminCouponView.as_view()),
    path('vendor',VendorListView.as_view()),
    path('vendor/<int:pk>',VendorlistView.as_view()),
    path('vendor/',VendorNameView.as_view()),
    path('sliders', AdminSlidersCreateView.as_view()),
    path('sliders/', Admin_Slider_List.as_view()),
    path('slider', Admin_Sliders_list.as_view()), 
    path('sliders/<int:pk>', AdminSlidersView.as_view()),
    path('send-otp', SendOtpView.as_view()),
    
    
    
    
    
   
    
    # path('reset-password', ResetPasswordView.as_view()),
]