from django.core.management import BaseCommand
from BlogApp.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create tag")
        tag_names = [
            ('Технические теги'),
            ('Мета теги'),
            ('Пользовательские теги'),
        ]
        tags = [Tag(name=name) for name in tag_names]
        Tag.objects.bulk_create(tags)

        self.stdout.write("Done")