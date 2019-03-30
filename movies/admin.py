from django.contrib import admin
from movies.models import Movie, Theater, Showing, Save
# Register your models here.


# admin.site.register(Movie)
#

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')
    date_hierarchy = 'release_date'
    list_filter = ('release_date',)


@admin.register(Theater)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


@admin.register(Showing)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater')


@admin.register(Save)
class MovieAdmin(admin.ModelAdmin):
    list_filter = ('date', 'saved_by')
