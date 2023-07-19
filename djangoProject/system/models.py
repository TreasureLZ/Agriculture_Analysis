from django.db import models

class Agriculture(models.Model):
    area =  models.CharField(verbose_name='省市',max_length=255)
    value = models.CharField(verbose_name='数值',max_length=255)
    unit = models.CharField(verbose_name='单位',max_length=255)
    zb = models.CharField(verbose_name='指标',max_length=255)
    updateTime = models.CharField(verbose_name='更新年份',max_length=255)

    class Meta:
        verbose_name = "农业数据"
        verbose_name_plural = "农业数据"
        db_table = "agriculture"

class Meteorology(models.Model):
    city = models.CharField(verbose_name='城市',max_length=255)
    month = models.CharField(verbose_name='月份',max_length=255)
    avg_max_temperature = models.CharField(verbose_name='平均最高气温',max_length=255)
    avg_min_temperature = models.CharField(verbose_name='平均最低气温',max_length=255)
    avg_precipitation = models.CharField(verbose_name='平均降水量',max_length=255)
    histroy_max_temperature = models.CharField(verbose_name='历史最高气温',max_length=255)
    histroy_min_temperature = models.CharField(verbose_name='历史最低气温',max_length=255)

    class Meta:
        verbose_name = "气候数据"
        verbose_name_plural = "气候数据"
        db_table = "meteorology"