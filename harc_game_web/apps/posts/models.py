from django.db import models, IntegrityError
from django.utils.text import slugify
from django.utils import timezone

from apps.users.models import HarcgameUser


class Post(models.Model):
    """
    Model postu

    Informacje, które będą zamieszczane dzień po dniu trwania Harcapo, które będa budować fabułę, przypominać o zadaniach itd.
	Atrybuty:
		Id postu (generowane automatycznie)
		Data (dzień i godzina)
		Tytuł
		Treść
		Autor
		Link do filmiku/obrazu
    """

    slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True)
    date_time = models.DateTimeField('Data utworzenia', blank=True)
    pub_date_time = models.DateTimeField('Kiedy ma być opublikowany', default=timezone.now)
    title = models.CharField('Tytuł', max_length=200)
    content = models.TextField('Treść', help_text='Można używać tagów HTML')
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    link1 = models.CharField('Link 1', max_length=400, null=True, default="", blank=True)
    link2 = models.CharField('Link 2', max_length=400, null=True, default="", blank=True)
    link3 = models.CharField('Link 3', max_length=400, null=True, default="", blank=True)

    # Auto-generate slug
    def slugify(self, i=None):
        slug = self.date_time.strftime("%Y-%m-%d-")+slugify(self.title)
        if i is not None:
            slug += "-%d" % i
        return slug

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            # Newly created object, so set timestamp and slug
            self.date_time = timezone.now()
            self.slug = self.slugify()

            # try to save
            try:
                return super(Post, self).save(*args, **kwargs)
            except IntegrityError:
                pass

            # Ensure the slug is uniqe
            slugs = set(
                type(self)
                ._default_manager.filter(slug__startswith=self.slug)
                .values_list("slug", flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(i)
                if slug not in slugs:
                    self.slug = slug
                    return super(Post, self).save(*args, **kwargs)
                i += 1
        else:
            # update
            return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - created by {self.user}'
