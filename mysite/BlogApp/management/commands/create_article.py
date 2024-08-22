import random
from datetime import  datetime
from typing import Sequence
from django.core.management import BaseCommand
from BlogApp.models import Article, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create article")
        tags: Sequence[Tag] = Tag.objects.only("id").all()
        article, created = Article.objects.get_or_create(
            tittle='Статья 1',
            content='Информационный ',
            pub_date=datetime.now(),
            author_id=1,
            category_id=3,
        )
        for tag in tags:
            article.tags.add(tag)
        article.save()
        self.stdout.write("Created article")