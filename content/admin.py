from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from content.models import CImages, Menu, Content, Ccomment


class ContentImageInline(admin.TabularInline):
    model = CImages
    extra = 5

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'image_tag', 'status', 'create_at']
    list_filter = ['status', 'type']
    inlines = [ContentImageInline]
    prepopulated_fields = {'slug': ('title',)}

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'title', 'image_tag']


class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'status')

class CcommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','content','user','status']
    list_filter = ['status']

admin.site.register(Ccomment, CcommentAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Content, ContentAdmin)