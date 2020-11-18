from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from apps.users.models import HarcgameUser
from apps.tasks.models import UploadedFile

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
    
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    date_time = models.DateTimeField('Data utworzenia')
    pub_date_time = models.DateTimeField('Kiedy ma być opublikowany', help_text='YYYY-MM-DD HH:mm:ss')
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(HarcgameUser, on_delete=models.RESTRICT, null=True, default=None)
    link1 = models.CharField(max_length=400, null=True, default="", blank=True)
    link2 = models.CharField(max_length=400, null=True, default="", blank=True)
    link3 = models.CharField(max_length=400, null=True, default="", blank=True)
    
    # Auto-generate slug
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
            self.date_time = timezone.now()
        super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.title} - created by {self.user}'
