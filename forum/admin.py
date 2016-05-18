from django.contrib import admin

from .models import Category, Thread, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_order')
    list_display_links = ('name', )
    list_editable = ['list_order',]

    class Media:
        js = ['js/jquery-1.11.0.min.js',
            'js/jquery-ui-1.10.4.custom.min.js', 
            'js/admin-list-reorder.js',]
        css = { 'all' : ['css/dynamic_inlines_with_sort.css'], }



admin.site.register(Category, CategoryAdmin)
admin.site.register(Thread)
admin.site.register(Post)
