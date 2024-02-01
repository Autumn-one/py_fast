import sys
import time

# 基本的游戏设置
class Game:
    def __init__(self):
        self.player = Player()
        self.scenes = {
            "start": StartScene(),
            "forest": ForestScene(),
            "river": RiverScene(),
            "mountain": MountainScene(),
            "end": EndScene()
        }
        self.current_scene = self.scenes["start"]

    def play(self):
        print("Welcome to the Adventure Game!")
        while not isinstance(self.current_scene, EndScene):
            self.current_scene = self.current_scene.enter(self.player)
            if self.player.health <= 0:
                print("You have died. Game Over.")
                sys.exit(0)
        print("Congratulations, you have completed the adventure!")

# 玩家类
class Player:
    def __init__(self):
        self.health = 100
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def is_alive(self):
        return self.health > 0

# 场景基类
class Scene:
    def enter(self, player):
        raise NotImplementedError("Subclass must implement abstract method")

# 各种场景
class StartScene(Scene):
    def enter(self, player):
        print("You find yourself in a small village. Where would you like to go?")
        print("1. The forest")
        print("2. The river")
        print("3. The mountain")
        choice = input("> ")

        if choice == "1":
            return game.scenes["forest"]
        elif choice == "2":
            return game.scenes["river"]
        elif choice == "3":
            return game.scenes["mountain"]
        else:
            print("Invalid choice.")
            return self

class ForestScene(Scene):
    def enter(self, player):
        print("You are in a dark, dense forest. You hear something moving.")
        print("1. Investigate the sound")
        print("2. Return to the village")
        choice = input("> ")

        if choice == "1":
            print("You found a wild animal! It attacks you.")
            player.health -= 10
            return game.scenes["start"] if player.is_alive() else game.scenes["end"]
        elif choice == "2":
            return game.scenes["start"]
        else:
            print("Invalid choice.")
            return self

class RiverScene(Scene):
    def enter(self, player):
        print("You are by a beautiful river. There's a boat here.")
        print("1. Take the boat and row across")
        print("2. Return to the village")
        choice = input("> ")

        if choice == "1":
            print("You row across the river safely.")
            player.add_item("Boat")
            return game.scenes["start"]
        elif choice == "2":
            return game.scenes["start"]
        else:
            print("Invalid choice.")
            return self

class MountainScene(Scene):
    def enter(self, player):
        print("You are at the base of a towering mountain.")
        print("1. Climb the mountain")
        print("2. Return to the village")
        choice = input("> ")

        if choice == "1":
            if "Boat" in player.inventory:
                print("You use the boat to slide down the mountain safely.")
                return game.scenes["end"]
            else:
                print("The climb is too dangerous and you fall.")
                player.health = 0
                return game.scenes["end"]
        elif choice == "2":
            return game.scenes["start"]
        else:
            print("Invalid choice.")
            return self

class EndScene(Scene):
    def enter(self, player):
        if player.is_alive():
            print("You have survived the adventure!")
        else:
            print("You did not survive the adventure.")
        return self

# 启动游戏
game = Game()
game.play()
