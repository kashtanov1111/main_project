from fileinput import filename
import random
import os
from django.core.files.storage import FileSystemStorage 
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from config.aws.download.utils import AWSDownload
from config.utils import unique_slug_generator, get_filename
from config.storage_backends import ProtectedMediaStorage

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,6432435789)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(
        new_filename=new_filename,
        final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)
    
    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                    Q(description__icontains=query) | 
                    Q(price__icontains=query) |
                    Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)
    def all(self):
        return self.get_queryset().active()
    def featured(self):
        return self.get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    def search(self, query):
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image       = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    is_digital  = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)

def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = 'product/{slug}/{id}/'.format(slug=slug, id=id_)
    return location + filename
        

class ProductFile(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    name            = models.CharField(max_length=120, null=True, blank=True )
    file            = models.FileField(
                        upload_to=upload_product_file_loc, 
                        storage=ProtectedMediaStorage()
                        )#FileSystemStorage(location=settings.PROTECTED_ROOT)
    free            = models.BooleanField(default=False)
    user_required   = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file.name)

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def get_default_url(self):
        return self.product.get_absolute_url()

    def generate_download_url(self):
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
        region = getattr(settings, 'S3DIRECT_REGION')
        access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
        secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        if not secret_key or not access_key or not bucket or not region :
            return '/product-not-found/'
        path = 'protected/{file_path}'.format(file_path=str(self.file))
        aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path, new_filename=self.display_name)
        return file_url


    def get_download_url(self):
        return reverse('products:download',
                    kwargs={'slug': self.product.slug, 'pk': self.pk}
                    )