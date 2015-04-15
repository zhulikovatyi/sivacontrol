from django.db import models

class Gender(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Gender(id=%d, title='%s')>" % (self.id, self.title)

class Banner(models.Model):
    title = models.CharField(max_length=128)
    # url = models.CharField(max_length=256)
    genders = models.ManyToManyField(Gender)
    url = models.FileField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.title, self.url)

    def __repr__(self):
        return "<Banner(id=%d, title='%s', url='%s')>" % (self.id, self.title, self.url)