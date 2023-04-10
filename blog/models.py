from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.conf import settings
# Create your models here.


class Post(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.FileField(null=True, blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]


# def create_slug(instance,new_slug=None):
#     slug=slugify(instance.title)
#     if new_slug is not None:
#         slug=new_slug
#     qs=Post.objects.filter(slug).order_by("-id")
#     exists=qs.exists()
#     if exists:
#         new_slug="%s-%s" %(slug,qs.first().id)
#         return create_slug(instance,new_slug=new_slug)
#     return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    # if not instance.slug:
    #     instance.slug=create_slug(instance)
    slug = slugify(instance.title)
   # "Tesla item 1" -> "tesla-item-1"
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" % (slug, instance.id)
    instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)
