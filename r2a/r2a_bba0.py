"""
@Grupo 6

@Giovanni - 202014280
@Caio - 211036034
@Marcello - 211038781

Implementação do algoritmo BBA-0.
"""

from player.parser import *
from r2a.ir2a import IR2A


class R2A_BBA0(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []
        #Reservatório do buffer, definido como 10% de sua capacidade
        self.reservoir = self.whiteboard.get_max_buffer_size()*0.1
        #Preenchimento atual do buffer
        self.current_buffer = self.whiteboard.get_playback_buffer_size()
        #Taxa atual
        self.current_rate = self.whiteboard.get_playback_qi()

    def handle_xml_request(self, msg):
        #Envia a mensagem de requisição do mpd para a camada ConnectionHandler, sem modificação.
        self.send_down(msg)

    def handle_xml_response(self, msg):
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        self.send_up(msg)

    def rate_function(self, b):
        #Inclinação da reta da função de taxa
        m = (self.qi[19] - self.qi[0])/(self.whiteboard.get_max_buffer_size()*0.9 - self.reservoir)

        #Retorna a recomendação da nova taxa
        return m*(b - self.reservoir) + self.qi[0]

    def handle_segment_size_request(self, msg):
        if len(self.current_buffer) > 0:
            if self.current_buffer[-1][1] <= self.reservoir:
                #Qualidade requisitada é Rmin, a fim de preencher o reservatório do buffer.
                msg.add_quality_id(self.qi[0])

            elif self.current_buffe[-1][1] >= self.whiteboard.get_max_buffer_size()*0.9:
                #Qualidade requisitada é Rmax, pois o buffer está mais de 90% preenchido.
                msg.add_quality_id(self.qi[19])

            else:
                if rate_function(self.current_buffer[-1][1]) > self.current_rate[-1][1]:
                    #Se a taxa recomendada for maior que a próxima taxa, ela será atualizada
                    for i in self.qi:
                        if rate_function(self.current_buffer[-1][1]) > i:
                            msg.add_quality_id(i)
                
                elif rate_function(self.current_buffer[-1][1]) < self.current_rate[-1][1]:
                    #Se a taxa recomendada for menor que a taxa anterior, esta será atualizada
                    for i in self.qi:
                        if rate_function(self.current_buffer[-1][1]) < i:
                            msg.add_quality_id(i)
                
                else:
                    #Se a taxa recomendada estiver dentro do intervalo aberto (Rate-, Rate+), ela não será atualizada
                    msg.add_quality_id(self.current_rate[-1][1])
        else:
            msg.add_quality_id(self.qi[0])


        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass


