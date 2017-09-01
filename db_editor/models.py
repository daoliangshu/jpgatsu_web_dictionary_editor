from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class DictionaryEntry(models.Model):
    lv_choices = (
        (0, 'Non Defined'),
        (1, 'Level1'),
        (2, 'Level2'),
        (3, 'Level3'),
        (4, 'Level4'),
        (5, 'Level5(easiest)'),
    )

    thematic_choices = (
        (-1, 'Non Defined'),
        (0, 'Consummer Society'),
        (1, 'Economy'),
        (2, 'Science'),
        (3, 'Quantity'),
        (4, 'Body Beauty'),
        (5, 'Shops'),
        (6, 'Animals'),
        (7, 'Food'),
        (8, 'Education'),
        (9, 'Computer'),
        (10, 'Justice'),
        (11, 'Politique'),
        (12, 'Programmation'),
        (13, 'Nature'),
        (14, 'Body'),
        (15, 'Weather'),
        (16, 'Clothes'),
        (17, 'Colors'),
        (18, 'Numbers'),
        (19, 'Time'),
        (20, 'Family'),
        (21, 'Professional'),
        (22, 'Society'),
        (23, 'Culture'),
        (24, 'Medical'),
        (25, 'Trip'),
        (26, 'Leisure'),
        (27, 'Opinion'),
    )

    entry_id = models.AutoField(primary_key=True, db_column="_id")
    jp_1 = models.CharField(max_length=255, null=True, blank=True)
    jp_2 = models.CharField(max_length=255, null=True, blank=True)
    zh_1 = models.CharField(max_length=255, null=True, blank=True)
    fr_1 = models.CharField(max_length=255, null=True, blank=True)
    fr_2 = models.CharField(max_length=255, null=True, blank=True)
    en_1 = models.CharField(max_length=255, null=True, blank=True)
    lesson = models.IntegerField(null=True)
    thematic = models.IntegerField(null=True, choices=thematic_choices)
    lv = models.IntegerField(null=True, choices=lv_choices)

    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        print('DictionaryEntry:{fr_1:' + str(self.fr_1) + ",{jp_1:" + str(self.jp_1) + "}," + "{jp_2:" + str(self.jp_2))


class DictionaryBackUpEntry(models.Model):
    lv_choices = (
        (0, 'Non Defined'),
        (1, 'Level1'),
        (2, 'Level2'),
        (3, 'Level3'),
        (4, 'Level4'),
        (5, 'Level5(easiest)'),
    )

    thematic_choices = (
        (-1, 'Non Defined'),
        (0, 'Consummer Society'),
        (1, 'Economy'),
        (2, 'Science'),
        (3, 'Quantity'),
        (4, 'Body Beauty'),
        (5, 'Shops'),
        (6, 'Animals'),
        (7, 'Food'),
        (8, 'Education'),
        (9, 'Computer'),
        (10, 'Justice'),
        (11, 'Politique'),
        (12, 'Programmation'),
        (13, 'Nature'),
        (14, 'Body'),
        (15, 'Weather'),
        (16, 'Clothes'),
        (17, 'Colors'),
        (18, 'Numbers'),
        (19, 'Time'),
        (20, 'Family'),
        (21, 'Professional'),
        (22, 'Society'),
        (23, 'Culture'),
        (24, 'Medical'),
        (25, 'Trip'),
        (26, 'Leisure'),
        (27, 'Opinion'),
    )

    entry_id = models.IntegerField(db_column="backup_id")
    jp_1 = models.CharField(max_length=255, null=True, blank=True)
    jp_2 = models.CharField(max_length=255, null=True, blank=True)
    zh_1 = models.CharField(max_length=255, null=True, blank=True)
    fr_1 = models.CharField(max_length=255, null=True, blank=True)
    fr_2 = models.CharField(max_length=255, null=True, blank=True)
    en_1 = models.CharField(max_length=255, null=True, blank=True)
    lesson = models.IntegerField(null=True)
    thematic = models.IntegerField(null=True, choices=thematic_choices)
    lv = models.IntegerField(null=True, choices=lv_choices)

    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        print('DictionaryBackUpEntry:{fr_1:' + str(self.fr_1) + "},{jp_1:" + str(self.jp_1) + "}," + "{jp_2:" + str(
            self.jp_2)) + "}"

    def _thematic(self):
        return self.thematic


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
