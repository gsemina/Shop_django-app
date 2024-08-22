from django.core.management import BaseCommand
from BlogApp.models import Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create author")
        authors_names = [
            ('Ivan', 'author 1'),
            ('Boris', 'author 2'),
            ('Roman', 'author 3'),
        ]
        authors = [Author(name=name, bio=bio) for name, bio in authors_names]
        Author.objects.bulk_create(authors)

        self.stdout.write("Done")