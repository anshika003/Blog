from django.contrib import admin
from blog.models import post, BlogComment

# Register your models here.
admin.site.register((BlogComment))
@admin.register(post)

class postAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js',)
