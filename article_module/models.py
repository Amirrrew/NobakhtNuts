from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from account_module.models import User
from ckeditor.fields import RichTextField


class Article(models.Model):
    title = models.CharField(max_length=1000,verbose_name='عنوان مقاله')
    banner = models.ImageField(upload_to='article_banners' ,null=True ,blank=True ,verbose_name='بنر مقاله')
    view = models.PositiveIntegerField(default=0 ,verbose_name='بازدید')
    created_at = models.DateTimeField(auto_now_add=True,db_index=True ,verbose_name='تاریخ آپلود')
    author = models.ForeignKey(User,on_delete=models.CASCADE ,verbose_name='نویسنده')
    desc = models.TextField(null=True ,blank=True ,verbose_name='توضیحات کوتاه')
    time_to_read = models.IntegerField(default=0 ,verbose_name='زمان برای خواندن')
    content = RichTextUploadingField()
    is_active = models.BooleanField(default=True ,db_index=True)
    slug = models.SlugField(null=True ,blank=False ,unique=True ,verbose_name='عنوان در url')

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'