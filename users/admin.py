from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from .models import User

from .models import User, AdminProfile, CustomerProfile
# Register your models here.

class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    fk_name = 'user'


class AdminUserAdmin(BaseUserAdmin):
    fieldsets = (
        (('User Credentials'), {'fields': ('username', 'password', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','admin',
                                       )}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'admin',),
        }),
    )
    list_display = ('id', 'username', 'email', 'date_joined', 'is_staff')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username',)
    ordering = ('username',)
    inlines = (AdminProfileInline, )
    list_select_related = ('Admin_profile',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(Q(admin=True) | Q(is_staff=True))  # HERE it is the flag for differentiating between Client and Partner

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AdminUserAdmin, self).get_inline_instances(request, obj)
    # list_select_related = ('profile',)

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    fk_name = 'user'

class CustomerUserAdmin(BaseUserAdmin):
    fieldsets = (
        (('User Credentials'), {'fields': ('username', 'password', 'email')}),
        (('Permissions'), {'fields': ('is_active','customer')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'customer',),
        }),
    )
    list_display = ('id', 'username', 'email', 'date_joined', 'is_staff')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username',)
    ordering = ('username',)
    inlines = (CustomerProfileInline, )
    list_select_related = ('Customer_profile',)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(customer=True)  # HERE it is the flag for differentiating between Client and Partner

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomerUserAdmin, self).get_inline_instances(request, obj)

    # list_select_related = ('profile',)



class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'

class CustomerUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Customer'


admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(CustomerUser, CustomerUserAdmin)
