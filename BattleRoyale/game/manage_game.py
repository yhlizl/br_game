# manage_game.py
import argparse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
import django
import os
import sys
from django.conf import settings
import asyncio
import websockets
import nest_asyncio
sys.path.append('./BattleRoyale')
print(sys.path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BattleRoyale.settings')
django.setup()
# Use settings here
print(settings.CHANNEL_LAYERS)
class GameServer:
    def __init__(self):
        self.group_name = "game"
        self.channel_layer = get_channel_layer()

    def start(self):
        self.game_state = "running"
        print("Server started")
        self.send_message(json.dumps({"action": "Server started"}))
    
    def get_info(self):
        self.send_to_server(json.dumps({"action": "get_info"}))

    def start_game(self):
        if self.game_state == "running":
            print("Game started")
            self.send_message(json.dumps({"action": "Game started"}))
        else:
            print("Server is not running")

    def start_practice(self, practice):
        if self.game_state == "running":
            if practice:
                print("Practice mode started")
                self.send_message(json.dumps({"action": "Practice mode started"}))
            else:
                print("Practice mode stopped")
                self.send_message(json.dumps({"action": "Practice mode stopped"}))
        else:
            print("Server is not running")

    def reset(self):
        self.game_state = "stopped"
        print("Game reset")
        self.send_message(json.dumps({"action": "Game reset"}))

    def send_message(self, message):
        # Use the group name to send a message
        print("Sending message:", message)
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "game.message",
            "text": message
        })
    def send_to_server(self, message):
        nest_asyncio.apply()
        asyncio.run(self._send_message(message))


    async def _send_message(self, message):
        uri = "ws://localhost:8787/"  # Replace with your WebSocket URL
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)

def main():
    parser = argparse.ArgumentParser(description='Manage the game server.')
    parser.add_argument('command', choices=['start', 'game', 'practice', 'reset', 'info'], help='the command to execute')
    parser.add_argument('--practice', type=bool, default=False, help='start or stop practice mode')

    args = parser.parse_args()

    server = GameServer()

    if args.command == 'start':
        server.start()
    elif args.command == 'game':
        server.start_game()
    elif args.command == 'practice':
        server.start_practice(args.practice)
    elif args.command == 'reset':
        server.reset()
    elif args.command == 'info':
        server.get_info()

if __name__ == '__main__':
    main()