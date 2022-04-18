from django.db import models

# Create your models here.
import email
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from colorfield.fields import ColorField
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
# Create your models here.
choices=(
    ('Admin',"Admin"), 
    ('Vendor','Vendor'),
    ('Customer','Customer'),
)



class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None,is_superuser=False,  is_staff=False, is_active=True,**fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.name = name
        user.set_password(password)  # change password to hash
        # user.profile_picture = profile_picture
   

        user.staff = is_staff
        user.active = is_active
        user.is_superuser = is_superuser
        
        user.save(using=self._db,**fields)
        return user

    def create_staffuser(self, email,  name, password=None):
        user = self.create_user(
            email,
            name,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            name,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.is_superuser = True
        user.is_staff=True
        user.save()
        return user
Country=(
    ('India','India'),
)
state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
class User(AbstractUser):
   
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=14,blank=True)
    email = models.CharField(unique=True,max_length=200)
    image=models.ImageField(upload_to ='uploads/', default="")
    user_type=models.CharField(choices=choices,max_length=300,default="Customer")
    permissions=models.BooleanField(null=True,blank=True)

    # vendor
    store_name=models.CharField(max_length=250,null=True,blank=True)
    address1=models.CharField(max_length=1000,null=True,blank=True)
    address2=models.CharField(max_length=1000,null=True,blank=True)
    country_vendor=models.CharField(choices=Country,max_length=100,null=True,blank=True)
    state = models.CharField(choices=state_choices,max_length=255,null=True,blank=True)
    city_town=models.CharField(max_length=500,null=True,blank=True)
    postcode_zip=models.CharField(max_length=100,null=True,blank=True)
    Store_Phone=models.CharField(null=True,blank=True,max_length=200)
    Direct_Number=models.IntegerField(null=True,blank=True)
    Website_address=models.CharField(max_length=1000,null=True,blank=True)
    Company_Incorporation=models.FileField(upload_to="VendorRegsiter/",null=True,blank=True)
    FSSAI_License=models.FileField(upload_to="VendorRegsiter/",null=True,blank=True)
    GST_Number=models.FileField(upload_to="VendorRegsiter/",null=True,blank=True)
    Recall_Plan=models.FileField(upload_to="VendorRegsiter/",null=True,blank=True)

    Fax=models.CharField(max_length=100,null=True,blank=True)
    City = models.CharField(max_length=100,null=True,blank=True)
    Country_cus=models.CharField(max_length=1000,null=True,blank=True)
    Zip=models.CharField(max_length=100,null=True,blank=True)
    Address=models.CharField(max_length=100,null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()
    def __str__(self):
        return str(self.name)
    
Product_Limitations = (
        ('Unlimited', 'Unlimited'),
        ('Limited', 'Limited'),
    )
class Vendor_subs(models.Model):

    Title  = models.CharField(max_length=100,null=True,blank=True)
    Currency_Symbol  = models.CharField(max_length=10, default="₹",null=True,blank=True)
    currency_code = models.CharField(max_length=10,null=True,blank=True)
    Cost  = models.CharField(max_length=100,null=True,blank=True)
    Days  = models.CharField(max_length=100,null=True,blank=True)
    Product_Limitations = models.CharField(choices=Product_Limitations,max_length=250,null=True,blank=True)
    Details =models.TextField(max_length=250,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Vendor_subs"
    
Type_status = (
        ('Discount by Percentage', 'Discount by Percentage'),
        ('Discount by Amount', 'Discount by Amount'),
    )

Qty_status = (
        ('Unlimited', 'Unlimited'),
        ('Limited', 'Limited'),
    )




class Admin_Coupon(models.Model):

    Code = models.CharField(max_length=100,null=True,blank=True)
    Amount=models.IntegerField(null=True,blank=True)
    Used=models.IntegerField(null=True,blank=True)
    Type= models.CharField(choices=Type_status,max_length=100,null=True,blank=True)
    Quantity= models.CharField(choices=Qty_status,max_length=100,null=True,blank=True)
    Status= models.BooleanField(null=True,blank=True)
    Start_Date=models.DateField(null=True,blank=True)
    End_Date=models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

  
    class Meta:
        db_table = "Coupon"

Payment_Status = (
        ('Active', 'Active'),
        ('Unactive', 'Unactive'),
    )

class Admin_tickets(models.Model):

    name=models.CharField(max_length=500,null=True,blank=True)
    email = models.EmailField(max_length=500,null=True,blank=True)
    subject = models.CharField(max_length=1000,null=True,blank=True)
    your_message = models.TextField(max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "Admin_Tickets"
    
class Admin_Disputes(models.Model):

    name=models.CharField(max_length=1000,null=True,blank=True)
    email=models.CharField(max_length=1000,null=True,blank=True)
    Order_Number = models.CharField(max_length=500,null=True,blank=True)
    Subject = models.CharField(max_length=1000,null=True,blank=True)
    Your_Message = models.TextField(max_length=2000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


slider_choices=(
    ('fadeIn','fadeIn'),
    ('fadeInDown','fadeInDown'),
    ('fadeInLeft','fadeInLeft'),
    ('fadeInRight','fadeInRight'),
    ('fadeInUp','fadeInUp'),
    ('flip','flip'),
    ('flipInX','flipInX'),
    ('flipInY','flipInY'),
    ('SlideInUp','SlideInUp'),
    ('SlideInLeft','SlideInLeft'),
    ('SlideInRight','SlideInRight'),
    ('SlideInDown','SlideInDown'),
    ('RollIn','RollIn'),
    

    )

Text_Position = (
        ('Left', 'Left'),
        ('Right', 'Right'),
        ('Center', 'Center'),
    )
class Admin_Sliders(models.Model):
    title_text=models.TextField(max_length=1000,null=True,blank=True)
    title_font_size=models.IntegerField(null=True,blank=True)
    title_font_color=ColorField(null=True,blank=True)
    title_animation=models.CharField(choices=slider_choices,max_length=1000,null=True,blank=True)
    subtitle_text=models.TextField(max_length=1000,null=True,blank=True)
    subtitle_font_size=models.IntegerField(null=True,blank=True)
    subtitle_font_color=ColorField(null=True,blank=True)
    subtitle_animation=models.CharField(choices=slider_choices,max_length=1000,null=True,blank=True)
    desc_text=models.TextField(max_length=1000,null=True,blank=True)
    desc_font_size=models.IntegerField(null=True,blank=True)
    desc_font_color=ColorField(null=True,blank=True)
    desc_animation=models.CharField(choices=slider_choices,max_length=1000,null=True,blank=True)
    image=models.ImageField(upload_to="media/slider",null=True,blank=True)
    link=models.CharField(max_length=1000,null=True,blank=True)
    text_position=models.CharField(choices=Text_Position,max_length=1000,null=True,blank=True)


class Shiprocket(models.Model):

    email=models.CharField(max_length=1000,null=True,blank=True)
    password=models.CharField(max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Slider_Font(models.Model):
    
    slider=models.ForeignKey(Admin_Sliders,on_delete=models.CASCADE)
    text=models.TextField(max_length=1000,null=True,blank=True)
    font_size=models.IntegerField(null=True,blank=True)
    font_color=ColorField(null=True,blank=True)
    animation=models.CharField(choices=slider_choices,max_length=1000,null=True,blank=True)




