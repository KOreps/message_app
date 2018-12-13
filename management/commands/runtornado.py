# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from tornado.ioloop import IOLoop
from message_store.tornado_app import application as messenger_app


class Command(BaseCommand):
    help = 'Start Tornado WebSocket server'

    def add_arguments(self, parser):
        parser.add_argument('--host', type=str)
        parser.add_argument('--port', type=str)

    def handle(self, *args, **options):
        host = options.get('host')
        port = options.get('port')
        if not host:
            raise CommandError('The host must be specified')
        if not port:
            raise CommandError('The port must be specified')
        self.stdout.write('Starting Messenger WebSocket server at ws://{0}:{1}'.format(host, port))
        messenger_app.listen(port, host)
        IOLoop.instance().start()
