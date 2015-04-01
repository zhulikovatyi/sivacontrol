from django.contrib import admin
from models import Banner, Gender

class BannerAdmin(admin.ModelAdmin):
    pass

class GenderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Banner, BannerAdmin)
admin.site.register(Gender, GenderAdmin)