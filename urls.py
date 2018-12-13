# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r"messages", views.MessageViewset, base_name="message")
router.register(r"incoming", views.IncomingMessageViewset, base_name="incoming_messages")
router.register(r"outgoing", views.OutgoingMessageViewset, base_name="outgoing_messages")

urlpatterns = [
    url(r'^', include(router.urls))
]