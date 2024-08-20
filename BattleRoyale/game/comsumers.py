from channels.generic.websocket import AsyncWebsocketConsumer
import json
from threading import Timer
class GameConsumer(AsyncWebsocketConsumer):
    games = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name

        # Initialize game state
        if self.room_name not in self.games:
            self.games[self.room_name] = {
                'players': {},
                'state': 'waiting',
                # Add other game state as needed
            }

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove player from game
        del self.games[self.room_name]['players'][self.channel_name]

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        # Update game state
        if action == 'move':
            self.games[self.room_name]['players'][self.channel_name]['position'] = text_data_json['position']
        elif action == 'attack':
            self.handle_attack(self.channel_name, text_data_json['target'])
        elif action == 'defend':
            self.handle_defend(self.channel_name)

        # Send new game state to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_state',
                'state': self.games[self.room_name],
            }
        )

    # Receive game state from room group
    async def game_state(self, event):
        state = event['state']

        # Send game state to WebSocket
        await self.send(text_data=json.dumps(state))

    def handle_attack(self, attacker, target):
        # Check if target is defending
        if self.games[self.room_name]['players'][target]['defending']:
            return

        # Otherwise, reduce target's health
        self.games[self.room_name]['players'][target]['health'] -= 1

        # Check if target is dead
        if self.games[self.room_name]['players'][target]['health'] <= 0:
            del self.games[self.room_name]['players'][target]

    def handle_defend(self, player):
        self.games[self.room_name]['players'][player]['defending'] = True

        # Set a timer to end defending after 1 second
        Timer(1, self.end_defend, args=[player]).start()

    def end_defend(self, player):
        self.games[self.room_name]['players'][player]['defending'] = False