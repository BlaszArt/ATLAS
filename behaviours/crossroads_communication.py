from spade.behaviour import CyclicBehaviour, FSMBehaviour, State

from behaviours.functions import AlgorithmFunctions
from models import messages_body_labels
from models.messages import CrossroadsMessages
import asyncio

class CrossroadsMessanger:
    WAITING_FOR_CHANGE_LIGHTS_NEED = "WAITING_FOR_CHANGE_LIGHTS_NEED"
    SEND_CFP = "SEND_CFP"
    WAITING_FOR_PROPOSALS = "WAITING_FOR_PROPOSALS"
    WAITING_FOR_INFORMS = "WAITING_FOR_INFORMS"

    # FIPA CONTRACT NET INTERACTION PROTOCOL... almost
    class NegotiatingProtocolInitiator(FSMBehaviour):

        async def on_start(self):
            self.add_state(name=CrossroadsMessanger.WAITING_FOR_CHANGE_LIGHTS_NEED,
                           state=self.ChangeLightsNeededSetData(), initial=True)
            self.add_state(name=CrossroadsMessanger.SEND_CFP, state=self.SendCFP())
            self.add_state(name=CrossroadsMessanger.WAITING_FOR_PROPOSALS, state=self.WaitingForProposals())
            self.add_state(name=CrossroadsMessanger.WAITING_FOR_INFORMS, state=self.WaitingForInforms())
            self.add_transition(source=CrossroadsMessanger.WAITING_FOR_CHANGE_LIGHTS_NEED,
                                dest=CrossroadsMessanger.SEND_CFP)
            self.add_transition(source=CrossroadsMessanger.SEND_CFP, dest=CrossroadsMessanger.WAITING_FOR_PROPOSALS)
            self.add_transition(source=CrossroadsMessanger.WAITING_FOR_PROPOSALS,
                                dest=CrossroadsMessanger.WAITING_FOR_INFORMS)
            await asyncio.sleep(15)

        class ChangeLightsNeededSetData(State):
            async def run(self):
                # print("[{}] jestem w stanie SETDATA".format(self.agent.jid))

                # collecting data for request of changing lights

                print('Jestem w ' + CrossroadsMessanger.WAITING_FOR_CHANGE_LIGHTS_NEED)

                AlgorithmFunctions.set_what_to_do_with_lights(self.agent)
                self.set_next_state(CrossroadsMessanger.SEND_CFP)

        class SendCFP(State):
            async def run(self):
                # print("[{}] jestem w stanie SEND CFP".format(self.agent.jid))

                await self.send_cfp_messages(self.build_cfp_messages())
                self.set_next_state(CrossroadsMessanger.WAITING_FOR_PROPOSALS)

            def build_cfp_messages(self):
                messages = []
                for neighbour_jid in self.agent.neighbours_jid.values():
                    print(neighbour_jid)
                    messages.append(CrossroadsMessages.build_cfp(neighbour_jid, self.agent))
                return messages

            async def send_cfp_messages(self, messages):
                for message in messages:
                    await self.send(message)

        class WaitingForProposals(State):
            def __init__(self):
                super().__init__()
                self.neigh_send_proposal_cnt = 0
                self.acc_proposal_jid = None

            async def run(self):
                # print("[{}] jestem w stanie WAITING PROPOSALS".format(self.agent.jid))
                print('CZEKAM PAŁKI')

                proposals = {}

                while self.not_all_neighoburs_send_proposals():
                    # timeout set randomly to let agent collect answers
                    msg = await self.receive(timeout=5)
                    self.if_proposal_add_to_proposals(msg, proposals)

                self.set_sender_of_best_proposal(proposals)

                await self.send_decisions_about_proposals(proposals)

                self.set_next_state(CrossroadsMessanger.WAITING_FOR_INFORMS)

            def not_all_neighoburs_send_proposals(self):
                return self.neigh_send_proposal_cnt != len(self.agent.neighbours_jid)

            def if_proposal_add_to_proposals(self, msg, proposals):
                if self.is_proposal(msg):
                    # msg.sender is fucked up, so its easier to get sender jid via formating it to string than from dict
                    proposals["{}".format(msg.sender)] = msg
                    self.neigh_send_proposal_cnt += 1

            def is_proposal(self, msg):
                return msg and msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.PROPOSE

            def set_sender_of_best_proposal(self, proposals):
                max_change_for = 0
                best_proposal_jid = None

                for neighbour_jid, proposal in proposals.items():
                    if proposal.get_metadata(messages_body_labels.can_you):
                        if max_change_for < proposal.get_metadata(messages_body_labels.change_by):
                            best_proposal_jid = neighbour_jid

                self.acc_proposal_jid = best_proposal_jid

            async def send_decisions_about_proposals(self, proposals):
                for neighbour_jid, proposal in proposals.items():
                    if self.is_accepted_proposal_sender(neighbour_jid):
                        # TODO: NASTAWIC TU COS W AGENCIE, ABY WIEDZIAL O ILE SKROCIC I/LUB WYDLUZYC KONKRETNE SWIATLA
                        # kierunek nastaw zna (self.cfp[messages_body_labels.direction]), ale czas na wydluzenie/skrocenie przychodzi z proposalem
                        # jesli direction z cfp jest inny niz aktualny kierunek zielonego to odjac czas od pozostalego do zmiany swiatla
                        await self.send(CrossroadsMessages.build_cfp_accept_proposal(proposal))
                    else:
                        await self.send(CrossroadsMessages.build_cfp_rejected_proposal(proposal))

            def is_accepted_proposal_sender(self, neighbour_jid):
                return self.acc_proposal_jid == neighbour_jid

        class WaitingForInforms(State):
            def __init__(self):
                super().__init__()
                self.neigh_send_inform_cnt = 0

            async def run(self):
                # print("[{}] jestem w stanie WAITING INFORM".format(self.agent.jid))

                while self.not_all_neighoburs_send_informs():
                    msg = await self.receive(timeout=5)
                    self.collect_inform_from_neighbour(msg)

                self.set_next_state(CrossroadsMessanger.WAITING_FOR_CHANGE_LIGHTS_NEED)

                # print("[{}] SZKONCZYLEM PROTOKOL!!!!".format(self.agent.jid))

            def not_all_neighoburs_send_informs(self):
                return self.neigh_send_inform_cnt != len(self.agent.neighbours_jid)

            def collect_inform_from_neighbour(self, msg):
                if self.is_inform(msg):
                    self.neigh_send_inform_cnt += 1

            def is_inform(self, msg):
                return msg and msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.INFORM

    class NegotiatingProtocolParticipant(CyclicBehaviour):
        async def run(self):
            reply = None
            msg = await self.receive()
            if msg:
                if self.is_cfp(msg):
                    reply = CrossroadsMessages.build_cfp_propose(participant=self.agent, received_cfp=msg)
                elif self.is_accept_proposal(msg):
                    reply = CrossroadsMessages.build_cpf_inform(received_message=msg, ok=True)
                elif self.is_reject_proposal(msg):
                    reply = CrossroadsMessages.build_cpf_inform(received_message=msg, ok=False)

                if reply:
                    await self.send(reply)

        def is_cfp(self, msg):
            return msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.CFP

        def is_accept_proposal(self, msg):
            return msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.ACCEPT_PROPOSAL

        def is_reject_proposal(self, msg):
            return msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.REJECT_PROPOSAL