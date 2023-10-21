from typing import List
from random import choice

# Constants

ROCK = 'rock'
PAPER = 'paper'
SCISSOR = 'scissor'

class RockPaperScissor:
    '''
        RockPaperScissor class acts as the brains for the classic game of Rock Paper Scissor
        If you're living under a rock pun intended :) and want to know the rules of the games, 
        check out the following (https://en.wikipedia.org/wiki/Rock_paper_scissors)
    '''

    def __init__(self, player_one_name:str, player_two_name='AI', winning_score=3) -> None:
        self.player_one = Player(player_one_name, winning_score=winning_score)
        self.player_two = Player(player_two_name, winning_score=winning_score)

        print(f'''
                Match Set: 
                Winning Point:- {winning_score}
                {self.player_one.name} VS {self.player_two.name}
            ''')
        
    def match(self, player_one_element, player_two_element):
        if player_one_element > player_two_element:
            self.player_one.score += 1
        elif player_one_element < player_two_element:
            self.player_two.score += 1

        print(f'''
------------------------------------------------------------------------------------------------------
                Current Score: 
                {self.player_one}:- {self.player_one.score}
                {self.player_two}:- {self.player_two.score}
------------------------------------------------------------------------------------------------------
            ''')
    
    def match_decided(self):
        return self.player_one.won or self.player_two.won
    
    def result(self):
        won_player:Player = self.player_one if self.player_one.won else self.player_two.won
        lost_player:Player = self.player_two if won_player is self.player_one else self.player_one

        print(f'''
                Congratulations {won_player.name.upper()} defeated {lost_player.name.upper()}
            ''')

class Element:
    def __init__(self, element_name:str, element_strength:str, element_weakness:str):
        self.element_name = element_name.lower()
        self.element_strength = element_strength.lower()
        self.element_weakness = element_weakness.lower()

    def __eq__(self, __value: object) -> bool:
        return self.element_name == __value.element_name

    def __gt__(self, __value: object) -> bool:
        return self.element_strength == __value.element_name
    
    def __lt__(self, __value: object) -> bool:
        return self.element_weakness == __value.element_name
    
    def __repr__(self) -> str:
        return f'Element: {self.element_name.title()}'
    
class Rock(Element):
    def __init__(self):
        super().__init__(ROCK, SCISSOR, PAPER)

class Paper(Element):
    def __init__(self):
        super().__init__(PAPER, ROCK, SCISSOR)

class Scissor(Element):
    def __init__(self):
        super().__init__(SCISSOR, PAPER, ROCK)

class Player:
    def __init__(self, name, winning_score=3) -> None:
        self.name = name
        self.score = 0
        self.winning_score = winning_score
    
    def __repr__(self) -> str:
        return f'Player - {self.name}, Score - {self.score}'

    def decide(self) -> Element:
        element = choice([Rock(), Paper(), Scissor()])
        print(self.name, 'Chose', element)
        return element
    
    @property
    def won(self) -> bool:
        return True if self.score >= self.winning_score else False
