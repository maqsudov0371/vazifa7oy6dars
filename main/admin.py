from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'is_active')
    list_filter = ('is_active',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Course)
class Coursedmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    prepopulated_fields = {'slug': ("title", )}



class HeaderImageInline(admin.TabularInline):
    model = HeaderImage
    extra = 1


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ("message", 'facebook', 'twitter', 'youtube', 'linkedin', 'address', 'phone1', 'phone2', 'email1', 'email2', 'view_image')
    list_editable = ('facebook', 'twitter', 'youtube', 'linkedin', 'address', 'phone1', 'phone2', 'email1', 'email2')
    inlines = [
        HeaderImageInline
    ]

    def view_image(self, header):
        return mark_safe(f'<img src="{header.logo.url}">')

    view_image.short_description = "Logo"


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class NewsAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(News, NewsAdmin)