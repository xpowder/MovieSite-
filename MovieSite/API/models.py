from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Categorys(models.Model):
    choices_categorys = [('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('science_fiction', 'Science Fiction'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('animation', 'Animation'),
        ('documentary', 'Documentary'),
        ('fantasy', 'Fantasy'),]


    name = models.CharField(max_length=15, choices=choices_categorys, unique=True)
     

    def __str__(self) -> str:
        return self.name



class Movies(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    puplish_date = models.DateField()
    movie_time = models.PositiveIntegerField(help_text="time in minutes")
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, related_name='movies', default='')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    image = models.ImageField(upload_to='image_movie')
    video = models.FileField(upload_to='videos', blank=True, null=True)


    def __str__(self) -> str:
        return self.title
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1,11)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user
    

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movies, related_name='watchlists')

    def __str__(self):
        return f"{self.user.username}'s Watchlist"

