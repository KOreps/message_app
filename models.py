# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sender",
        verbose_name="Отправитель"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receiver",
        verbose_name="Получатель"
    )

    body = models.TextField(
        verbose_name="Текст сообщения"
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отправки"
    )

    status = models.BooleanField(
        default=False,
        verbose_name="Прочитано"
    )

    class Meta:
        verbose_name="Сообщение"
        verbose_name_plural="Сообщения"
        ordering = ("-date", )

    def __str__(self):
        return "{} - {}({})".format(self.sender, self.receiver, self.date)