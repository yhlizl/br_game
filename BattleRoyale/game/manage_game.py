# manage_game.py
import argparse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class GameServer:
    def __init__(self):
        self.game_state = "stopped"
        self.channel_layer = get_channel_layer()

    def start(self):
        self.game_state = "running"
        print("Server started")
        self.send_message("Server started")

    def start_game(self):
        if self.game_state == "running":
            print("Game started")
            self.send_message("Game started")
        else:
            print("Server is not running")

    def start_practice(self, practice):
        if self.game_state == "running":
            if practice:
                print("Practice mode started")
                self.send_message("Practice mode started")
            else:
                print("Practice mode stopped")
                self.send_message("Practice mode stopped")
        else:
            print("Server is not running")

    def reset(self):
        self.game_state = "stopped"
        print("Game reset")
        self.send_message("Game reset")

    def send_message(self, message):
        async_to_sync(self.channel_layer.group_send)("game", {
            "type": "game.message",
            "text": message
        })

def main():
    parser = argparse.ArgumentParser(description='Manage the game server.')
    parser.add_argument('command', choices=['start', 'game', 'practice', 'reset'], help='the command to execute')
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

if __name__ == '__main__':
    main()