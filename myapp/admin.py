from django.contrib import admin
from myapp.models import Links,Match

# Register your models here.


class LinksInline(admin.TabularInline):
	model = Links
	# form = ProductForm
	# exclude = ['sku', 'weight', 'real_tracking_no', 'tracking_data']
	# readonly_fields = ('product_info', 'weight', 'shipping_cost', 'generate_order', 'dimensions')
	# fields = (
	# 	'product_info', 'name', 'quantity', 'price', 'weight', 'applied_weight', 'is_document','dimensions' ,'generate_order',)
	extra = 0

class MatchAdmin(admin.ModelAdmin):
	inlines = (LinksInline,)


admin.site.register(Match, MatchAdmin)