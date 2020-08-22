from django.contrib import admin
from .models import User, Post, Relation

# Register your models here.
admin.site.site_header = "Network Admin"
admin.site.site_title = "Network Admin Area"
admin.site.index_title = "Welcome to microblogging Admin"

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Relation)
