

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Admin_Sliders, Slider_Font, User, Vendor_subs,Admin_Coupon,Shiprocket
#from django.utils.translation import ugettext_lazy as _
from .forms import UserCreationForm
from django.utils.html import format_html

# Register your models here.

@admin.register(User)
class AdminUser(UserAdmin):
     add_form = UserCreationForm
     list_display = ("id", "name", "phone",'email','is_active','username')
     ordering = ['-id']
     exclude = ['username','first_name','last_name']



     readonly_fields = ("last_login", "date_joined")

     fieldsets = (
        ('Personal info', {'fields': ( 'email', 'password','user_type')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

     # add user form
     add_fieldsets = ((None, {
         'classes': ('wide', ),
         'fields': ('name', 'email', 'phone', 'user_type'),
     }), )

#     # display details

admin.site.register(Vendor_subs)
admin.site.register(Admin_Coupon)
admin.site.register(Admin_Sliders)
admin.site.register(Shiprocket)
# class Title_subtitle(admin.TabularInline):
#     model =Slider_Font

# @admin.register(Admin_Sliders)
# class AddSlidersAdmin(admin.ModelAdmin):
#     inlines = (Title_subtitle,)
