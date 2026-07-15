from django.contrib import admin

from product_module.models import Product, ProductCategory, ProductSubCategory, ProductBrand, PackageSize, \
    ProductFeature, ProductImage, ProductComment


class ProductFeatureAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 1

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title' ,'category' ,'price' ,'is_active' ,'is_available']
    list_editable = ['price' ,'is_active' ,]
    list_filter = ['is_active' ,'created_at']
    inlines = [ProductFeatureAdmin ,ProductImageAdmin]

class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title' ,'main_category' ,'is_active']
    list_editable = ['is_active' ,]
    list_filter = ['main_category' ,]

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user' ,'product' ,'created_at' ,'is_approved']
    list_editable = ['is_approved']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory , ProductSubCategoryAdmin)
admin.site.register(ProductBrand)
admin.site.register(PackageSize)
admin.site.register(ProductComment, ProductCommentAdmin)
