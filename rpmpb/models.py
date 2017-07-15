from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse


@python_2_unicode_compatible
class Tag(models.Model):
    slug_name = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug_name


@python_2_unicode_compatible
class Miniature(models.Model):
    slug_name = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=500, default="")
    description = models.CharField(max_length=2000, default="", blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # TODO: This feels weird. The model knows view details now
        return reverse('rpmpb:mini-detail', 
            kwargs={'slug': self.slug_name})

@python_2_unicode_compatible
class PhotoSession(models.Model):
    description = models.CharField(max_length=2000, default="", blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    miniature = models.ForeignKey(Miniature, on_delete=models.CASCADE)
    thumbnail = models.ImageField(blank=True, upload_to="images")
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.description


@python_2_unicode_compatible
class Album(models.Model):
    slug_name = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=500, default="", blank=True)
    description = models.CharField(max_length=2000, default="", blank=True)
    miniatures = models.ManyToManyField(Miniature, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField("self", blank=True, null=True)

    def __str__(self):
        return self.name

