from django.contrib import admin

from .models import Person, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_link_url')
    search_fields = ['title']
    def show_link_url(self, obj):
        return '<a href="{url}">{url}</a>'.format(url=obj.link)
    show_link_url.short_description = "Link"
    show_link_url.allow_tags = True

admin.site.register(Post, PostAdmin)
