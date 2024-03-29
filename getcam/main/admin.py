from django.contrib import admin

# Register your models here.
from main.models import *
admin.site.register(contact)

# admin.site.register(products)

admin.site.register(location)
admin.site.register(Orderitems)
admin.site.register(requested_delivary)

admin.site.register(reviews_of_product)
admin.site.register(faq_of_product)
admin.site.register(Order)
admin.site.register(ShippingOrder)
admin.site.register(Customer)
admin.site.register(essential_details)

admin.site.register(prize_chart)
admin.site.register(subscribedmaile)

class postimageadmin(admin.StackedInline):
        model = images_fiels


@admin.register(products)
class postadmin(admin.ModelAdmin):
    inlines = [postimageadmin]
    class Meta:
        model = products

@admin.register(images_fiels)
class postimageadmin(admin.ModelAdmin):
    pass
