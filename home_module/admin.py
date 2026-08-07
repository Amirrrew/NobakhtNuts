from django.contrib import admin

from home_module.models import SpecialEvents, LandingPage, Carousel, CarouselItem, HomeCards, CardBlock, Banner

admin.site.register(SpecialEvents)
admin.site.register(LandingPage)

class CarouselItemInline(admin.TabularInline):
    model = CarouselItem
    extra = 1

class CarouselAdmin(admin.ModelAdmin):
    inlines = [CarouselItemInline]

class CardBlockItemAdmin(admin.TabularInline):
    model = HomeCards
    extra = 1

class CardBlockAdmin(admin.ModelAdmin):
    inlines = [CardBlockItemAdmin]


admin.site.register(CardBlock ,CardBlockAdmin)
admin.site.register(Carousel ,CarouselAdmin)
admin.site.register(Banner)



