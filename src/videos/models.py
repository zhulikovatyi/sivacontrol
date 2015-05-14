from django.db import models

class Gender(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Gender(id=%d, title='%s')>" % (self.id, self.title)

class Banner(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(validators=[], max_length=256, default="Coming soon ...")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.title, self.url)

    def __repr__(self):
        return "<Banner(id=%d, title='%s', url='%s')>" % (self.id, self.title, self.url)

class AgeGroup(models.Model):
    start_boundary = models.IntegerField()
    stop_boundary = models.IntegerField()
    pass


class BannerWeight(models.Model):
    TOO_LOW = 0
    LOW = 1
    MIDDLE = 2
    HIGH = 3
    BANNER_WEIGHTS = (
        (TOO_LOW, 'Too Low'),
        (LOW, 'Low'),
        (MIDDLE, 'Middle'),
        (HIGH, 'High')
    )
    banner = models.ForeignKey(Banner, related_name='age_gender_weights')
    gender = models.ForeignKey(Gender)
    age_group = models.ForeignKey(AgeGroup)
    weight = models.IntegerField(choices=BANNER_WEIGHTS)