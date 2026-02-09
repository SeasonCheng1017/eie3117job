from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255) # name of the category
    slug = models.SlugField()               # address of the category
                                            # (typically at the end of URL)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Category, related_name='products', 
								on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'

    def get_image(self):
        if self.image:
            return 'http:localhost:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http:localhost:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http:localhost:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JEPG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('company', 'Company'),
        ('individual', 'Individual'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    nickname = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.nickname or self.user.username

class Job(models.Model):
    company = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='jobs',
        limit_choices_to={'user_type': 'company'},
    )
    title = models.CharField(max_length=255)
    requirement = models.TextField()
    duty = models.TextField()
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} @ {self.company.company_name or self.company.nickname or self.company.user.username}'

class Application(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'user_type': 'individual'},
    )
    message = models.TextField()
    cv = models.FileField(upload_to='cvs/')
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.applicant} -> {self.job}'