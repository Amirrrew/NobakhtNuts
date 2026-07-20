from django.contrib import admin

from home_module.models import SpecialEvents, SliderSlide, Carousel, CarouselItem

admin.site.register(SpecialEvents)
admin.site.register(SliderSlide)

class CarouselItemInline(admin.TabularInline):
    model = CarouselItem
    extra = 1

class CarouselAdmin(admin.ModelAdmin):
    inlines = [CarouselItemInline]

admin.site.register(Carousel ,CarouselAdmin)


