from EcoSimpy import DiscreteEventAgent
from .el_farol_bar_action_set import Strategy, RandomPlay, LikeCrowded, LikeSixtyPercent
import random

class Player(DiscreteEventAgent):

    def __init__(self, 
                 simulation, 
                 scenario,
                 agent_number, 
                 agent_def
                ):

        super().__init__(simulation,
                         scenario,
                         agent_number,
                         agent_def
                        )
        self.payoff = 0
        self.my_play = ""
        self.other_play = ""
        self.memory = [0]
        self.memory_recall = 10
        self.strategy = Strategy(self, self.memory_recall)
        self.selected_predictor = ""
        self.predictor_fitness = 0.0
        self.predictor_prediction = 0
        self.space = self.spaces["EFBGame"]


        ############## DEIXAR POR ENQUANTO ######
        # decisão atual
        self.my_play = "NOT GOING"

        # memória das frequências passadas
        self.memory = [random.randint(40, 70)]

        # quantidade máxima de memória
        self.memory_recall = 10

        # última previsão realizada
        #self.last_prediction = 50
        self.memory = [random.randint(40, 70)]

    def step(self):
        """ agent step """
        self.select_game()

    def select_game(self):
        """ The agent select a play from a strategy """
        self.game_payoff()
        selected_predictor = self.strategy.selected_predictor()
        self.selected_predictor = selected_predictor[0]
        self.predictor_fitness = selected_predictor[1][self.my_step]
        self.predictor_prediction = selected_predictor[2][self.my_step]
        self.my_play = self.strategy.select_game()

    def play(self):
        """ The agent plays a strategy - method my_play """
        return self.my_play

    def game_payoff(self):
        """ Get the game payoff """
        self.payoff = self.strategy.payoff(self.my_play)

    def get_frequency(self, frequency):
        """"Get the frequency in the bar """
        self.memory.append(frequency)
        self.strategy.get_frequency(frequency)








    # ##### ISSO DEVE SER EXCLUIDO DEPOIS ######
  
    # # SISTEMA DE PAYOFF

    # def game_payoff(self, attendance):

    #     comfort_limit = self.space.comfort_limit


    #     # foi ao bar
    #     if self.my_play == "GOING":

    #         # experiência boa
    #         if attendance <= comfort_limit:

    #             self.payoff += 1

    #         # experiência ruim
    #         else:

    #             self.payoff -= 1


    #     # ficou em casa
    #     else:

    #         # evitou lotação
    #         if attendance > comfort_limit:

    #             self.payoff += 1

    #         # perdeu uma boa noite
    #         else:

    #             self.payoff -= 1


    
    # # MEMORY UPDATE
  

    # def get_frequency(self, frequency):

    #     self.memory.append(frequency)

    #     # mantém memória limitada
    #     if len(self.memory) > self.memory_recall:

    #         self.memory.pop(0)




class RandomPlayer(Player):
    """ A player that makes random decisions """
    def __init__(self, simulation, scenario, agent_number, agent_def):
        super().__init__(simulation, scenario,  agent_number, agent_def)
        self.strategy = RandomPlay(self, self.memory_recall)

    def select_game(self):
        """Random selection of the game"""
        if random.random() > .5:
            self.my_play = "GOING"
        else:
            self.my_play = "NOT GOING"



class LikeCrowdedPlayer(Player):
    """ A player that likes crowded bars """
    def __init__(self, simulation, scenario,  agent_number, agent_def):
        super().__init__(simulation, scenario,  agent_number, agent_def)
        self.strategy = LikeCrowded(self, self.memory_recall)

    def select_game(self):
        """ The agent select a play from a strategy """
        selected_predictor = self.strategy.selected_predictor()
        self.selected_predictor = selected_predictor[0]
        self.predictor_fitness = selected_predictor[1][self.my_step]
        self.predictor_prediction = selected_predictor[2][self.my_step]
        self.my_play = self.strategy.select_game()


class LikeSixtyPercentPlayer(Player):
    """ A player that hopes the bar is not crowded """
    def __init__(self, simulation, scenario,  agent_number, agent_def):
        super().__init__(simulation, scenario,  agent_number, agent_def)
        self.strategy = LikeSixtyPercent(self, self.memory_recall)




# class RandomPlayer(Player):
#     """ Agente aleatório """

#     def step(self):

#         prediction = random.randint(40, 70)

#         self.last_prediction = prediction


#         if prediction <= self.space.comfort_limit:

#             self.my_play = "GOING"

#         else:

#             self.my_play = "NOT GOING"





class MeanPlayer(Player):
    """ Agente baseado em média """

    def step(self):

        prediction = sum(self.memory) / len(self.memory)

        self.last_prediction = prediction


        if prediction <= self.space.comfort_limit:

            self.my_play = "GOING"

        else:

            self.my_play = "NOT GOING"





class TrendPlayer(Player):
    """ Agente seguidor de tendência """

    def step(self):

        mem = self.memory


        # memória insuficiente
        if len(mem) < 2:

            prediction = mem[-1]

        else:

            trend = mem[-1] - mem[-2]

            prediction = mem[-1] + trend


        # limita previsão
        prediction = max(0, min(100, prediction))

        self.last_prediction = prediction


        if prediction <= self.space.comfort_limit:

            self.my_play = "GOING"

        else:

            self.my_play = "NOT GOING"





class ContrarianPlayer(Player):
    """ Agente anti-manada: Calcula a media e toma a decisão contrária """

    def step(self):

        last_attendance = self.memory[-1]


        # acredita em reversão
        if last_attendance > self.space.comfort_limit:

            prediction = last_attendance - 20

        else:

            prediction = last_attendance + 20


        prediction = max(0, min(100, prediction))

        self.last_prediction = prediction


        if prediction <= self.space.comfort_limit:

            self.my_play = "GOING"

        else:

            self.my_play = "NOT GOING"





class GrudgerPlayer(Player):
    """ Agente intolerante à superlotação """

    def __init__(self, simulation, model, agent_number, agent_def):

        super().__init__(
            simulation,
            model,
            agent_number,
            agent_def
        )

        # rodadas lotadas consecutivas
        self.overcrowded_count = 0

        # cooldown social
        self.cooldown = 0


    def step(self):

        # burnout social
        if self.cooldown > 0:

            # previsão simbólica
            self.last_prediction = 100

            self.my_play = "NOT GOING"

            self.cooldown -= 1

            return


        # comportamento normal
        prediction = sum(self.memory) / len(self.memory)

        self.last_prediction = prediction


        if prediction <= self.space.comfort_limit:

            self.my_play = "GOING"

        else:

            self.my_play = "NOT GOING"


    def get_frequency(self, frequency):

        super().get_frequency(frequency)


        # verifica lotação
        if frequency > self.space.comfort_limit:

            self.overcrowded_count += 1

        else:

            self.overcrowded_count = 0


        # perdeu a paciência
        if self.overcrowded_count >= 3:

            self.cooldown = 3

            self.overcrowded_count = 0




class FOMOPlayer(Player):
    """ Fear Of Missing Out """

    def __init__(self, simulation, model, agent_number, agent_def):

        super().__init__(
            simulation,
            model,
            agent_number,
            agent_def
        )

        self.fomo_trigger = False


    def step(self):

        # impulso emocional
        if self.fomo_trigger:

            self.last_prediction = 0

            self.my_play = "GOING"

            self.fomo_trigger = False

            return


        # comportamento normal
        prediction = sum(self.memory) / len(self.memory)

        self.last_prediction = prediction


        if prediction <= self.space.comfort_limit:

            self.my_play = "GOING"

        else:

            self.my_play = "NOT GOING"


    def game_payoff(self, attendance):

        # calcula payoff primeiro
        super().game_payoff(attendance)

        comfort_limit = self.space.comfort_limit


        # arrependimento
        if (
            self.my_play == "NOT GOING"
            and attendance <= comfort_limit
        ):

            self.fomo_trigger = True




class ReactivePlayer(Player):
    """ Win-Stay Lose-Shift """

    def __init__(self, simulation, model, agent_number, agent_def):

        super().__init__(
            simulation,
            model,
            agent_number,
            agent_def
        )

        # ação inicial aleatória
        self.last_action = random.choice([
            "GOING",
            "NOT GOING"
        ])

        # assume sucesso inicial
        self.last_result = 1


    def step(self):

        # venceu -> repete
        if self.last_result > 0:

            self.my_play = self.last_action

        # perdeu -> troca
        else:

            if self.last_action == "GOING":

                self.my_play = "NOT GOING"

            else:

                self.my_play = "GOING"


        # previsão simbólica
        if self.my_play == "GOING":

            self.last_prediction = 0

        else:

            self.last_prediction = 100


    def game_payoff(self, attendance):

        # salva payoff anterior
        old_payoff = self.payoff


        # usa payoff padrão
        super().game_payoff(attendance)


        # verifica resultado
        if self.payoff > old_payoff:

            self.last_result = 1

        else:

            self.last_result = -1


        # salva ação
        self.last_action = self.my_play




