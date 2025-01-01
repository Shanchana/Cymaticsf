from django.contrib import admin
from .models import*

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Assets)
admin.site.register(Entertainment)

# Register your models here.
