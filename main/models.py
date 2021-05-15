from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

THEME_CHOICES = [
    ('EL', 'Electronic'),
    ('IT', 'IT'),
    ('ED', 'Education'),
    ('CH', 'Charity'),
    ('GP', 'GreenPeace'),
]


class Company(models.Model):
    title = models.CharField(unique=True, max_length=100)
    description = RichTextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, related_name='companies')
    video_url = models.URLField(max_length=200)
    theme = models.CharField(max_length=2, choices=THEME_CHOICES, default='IT')
    goal = models.DecimalField(max_digits=7, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    date_finish = models.DateField()

    @property
    def price_display(self):
        return '${}'.format(self.goal)

    def __str__(self):
        return self.title


class Bonus(models.Model):
    money = models.CharField(max_length=20)


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return ''.join(self.title)


class Comment(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['published']

    def __str__(self):
        return f'Comment by {self.author.username}'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ['-value']


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.star} - {self.company}'


#  Users staff
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __str__(self):
        return f'{self.user.username} Profile'


class Photo(models.Model):
    # Misc Django Fields
    title = models.CharField("Title (optional)", max_length=200, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # Points to a Cloudinary image
    image = CloudinaryField('image')


