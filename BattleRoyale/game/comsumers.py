from channels.generic.websocket import AsyncWebsocketConsumer
import json
from threading import Timer

class GameConsumer(AsyncWebsocketConsumer):
    game = {
        'players': {},
        'state': 'waiting',
        # Add other game state as needed
    }

    async def connect(self):
        # Join game group
        await self.channel_layer.group_add(
            "game",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave game group
        await self.channel_layer.group_discard(
            "game",
            self.channel_name
        )

        # Remove player from game
        del self.game['players'][self.channel_name]

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        # Update game state
        if action == 'move':
            self.game['players'][self.channel_name]['position'] = text_data_json['position']
        elif action == 'attack':
            self.handle_attack(self.channel_name, text_data_json['target'])
        elif action == 'defend':
            self.handle_defend(self.channel_name)

        # Send new game state to WebSocket
        await self.send(text_data=json.dumps(self.game))
    # Receive message from game group
    async def game_message(self, event):
        message = event['text']

        if message == "Server started":
            self.game['state'] = 'running'
        elif message == "Game started":
            self.game['state'] = 'game'
        elif message == "Practice mode started":
            self.game['state'] = 'practice'
        elif message == "Practice mode stopped":
            self.game['state'] = 'running'
        elif message == "Game reset":
            self.game['state'] = 'waiting'
            self.game['players'] = {}

        # Send new game state to WebSocket
        await self.send(text_data=json.dumps(self.game))

    def handle_attack(self, attacker, target):
        # Check if target is defending
        if self.game['players'][target]['defending']:
            return

        # Otherwise, reduce target's health
        self.game['players'][target]['health'] -= 1

        # Check if target is dead
        if self.game['players'][target]['health'] <= 0:
            del self.game['players'][target]

    def handle_defend(self, player):
        self.game['players'][player]['defending'] = True

        # Set a timer to end defending after 1 second
        Timer(1, self.end_defend, args=[player]).start()

    def end_defend(self, player):
        self.game['players'][player]['defending'] = False