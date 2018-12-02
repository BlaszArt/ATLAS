from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from models.messages import CrossroadsMessages


class CrossroadsMessanger:
    #Ten ktory chce zmienic lub przedluzyc swiatla uzyje tego behavioura -
    class SendLightsChangeNeeded(OneShotBehaviour):
        def __init__(self, change_direction):
            super().__init__(self)
            self.change_direction = change_direction

        async def run(self):
            for message in self.build_messages(self.change_direction):
                await self.agent.send(message)

        def build_messages(self, change_direction):
            messages = [];
            for neighbour_jid in self.agent.presence.get_contacts().keys():
                messages.append(CrossroadsMessages.build_cfp(neighbour_jid, self.agent, change_direction, True, 15)) #todo jakos podliczyc ten czas (aktualnie 15) o ile zmienic i co chce zrobic (aktuanie True)
            return messages

    # todo jak sie doda thready (patrz messages.py) to trzeba odsylac wiadomosci na ten sam thread co przyszla
    class IteratedContractNetProtocol(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.CFP:
                    reply = CrossroadsMessages.build_cfp_propose(receiver = msg.sender,can_you=True,in_sec=10) #todo: za in_sec wartosc, o ktora agent proponuje, ze zadajacy mógłby skrocic/wydluzyc swiatla
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.PROPOSE:
                    pass # todo: accept-proposal lub cfp z nowymi danymi (nie wiem czy CFP nie wymusza uzycia State Machine)
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.ACCEPT_PROPOSAL:
                    reply = CrossroadsMessages.build_cpf_inform(receiver = msg.sender, ok = True) #zaakceptowana propozycja - wyslij inform, koniec protokolu
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.ACCEPT_PROPOSAL:
                    reply = CrossroadsMessages.build_cpf_inform(receiver=msg.sender, ok=False) #odrzucona propozycja - wyslij inform, koniec protokolu
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.INFORM:
                    pass
                if reply:
                    await self.agent.send(reply)



