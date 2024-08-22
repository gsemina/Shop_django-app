from django.contrib import admin
from .models import Tag, Article, Author, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = "pk", "name", 'bio'
    list_display_links = "pk", "name"
    search_fields = ["name",]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"
    search_fields = ["name",]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"
    search_fields = ["name",]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "pk", "title", 'content', "pub_date", "author", "category",
    list_display_links = "pk", "title"
    search_fields = ["title",]

