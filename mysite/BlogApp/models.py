from django.db import models
from django.urls import reverse


class Author(models.Model):
    """
    Модель Author содержит информацию об авторе статьи.
    """

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True)


class Category(models.Model):
    """
    Модель Category представляет категорию статьи.
    """

    name = models.CharField(max_length=40)


class Tag(models.Model):
    """
    Модель Tag представляет тэг, который можно назначить статье.
    """
    name = models.CharField(max_length=20)


class Article(models.Model):
    """
    Модель Article представляет статью.
    Атрибуты:
        title(CharField) — заголовок статьи.
        content(TextField) — содержимое статьи.
        pub_date (DateTimeField) — дата публикации статьи.
        author(ForeignKey) — автор статьи.
        category(ForeignKey) — категория статьи.
        tags(ManyToManyField) — тэги статьи.
            ManyToManyField, несколько тэгов для каждой статьи
    """

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tag')

    def __str__(self) -> str:
        return f"Article(pk={self.pk}, title={self.title!r})"

    def get_absolute_url(self):
        return reverse("BlogApp:article", kwargs={"pk": self.pk})
