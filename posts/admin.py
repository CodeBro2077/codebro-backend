from django.contrib import admin
from .models import Posts, Categories, Images

admin.site.register(Categories)
admin.site.register(Posts)
admin.site.register(Images)
