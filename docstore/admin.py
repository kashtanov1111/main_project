from django.contrib import admin

from .models import Store, Book, Publisher, Author

admin.site.register(Store)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)