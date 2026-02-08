from src.game import Game
from src.player import Player
from src.dans_bot import MyBot

bot = Player("Bot")
game = Game([bot, Player("Player")])
bot.assign_bot(game, MyBot)

game.start()
