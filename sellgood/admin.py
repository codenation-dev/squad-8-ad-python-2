from django.contrib import admin

from sellgood.models import Plan, Seller, Address, Sale


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'minimum_amount', 
                    'lower_percentage', 'higher_percentage')


class SellerAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'name', 'age', 'phone', 'email', 'plan')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'neighborhood', 'city', 'state', 
                    'number', 'complement', 'zipcode', 'seller')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'commission', 'seller')


admin.site.register(Plan, PlanAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Sale, SaleAdmin)
