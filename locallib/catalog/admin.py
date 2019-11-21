from django.contrib import admin

from catalog.models import Author, Genre, Book, BookInstance

admin.site.register(Book)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
                'last_name',
                'first_name',
                'date_of_birth',
                'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


# Register the Admin classes for Book using the decorator
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'display_genre')

#     def display_genre(self):
#         return ', '.join(genre.name for genre in self.genre.all()[:3])
#     display_genre.short_description = 'Genre'


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


admin.site.register(Genre)
# admin.site.register(BookInstance)
