from django.contrib import admin

# Register your models here.
from.models import Article

@admin.register(Article)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'sub_category', 'tags')  # Customize the displayed fields