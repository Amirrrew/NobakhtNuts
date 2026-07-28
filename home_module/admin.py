from django.contrib import admin

from home_module.models import SpecialEvents, SliderSlide, Carousel, CarouselItem, HomeCards, CardBlock

admin.site.register(SpecialEvents)
admin.site.register(SliderSlide)

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



