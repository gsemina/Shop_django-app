from django.contrib.auth.models import User

from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")
        users_info = User.objects.values_list("username", flat=True) #flat указываем, когда 1 элемент и нужно все в один список
        print(list(users_info))
        for us_info in users_info:
            print(us_info)
        # products_values = Product.objects.values("pk", "name")
        # for p_value in products_values:
        #     print(p_value)
        self.stdout.write("Done")