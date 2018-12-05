from spade.behaviour import CyclicBehaviour, FSMBehaviour, State

from behaviours.functions import AlgorithmFunctions
from models import messages_body_labels
from models.messages import CrossroadsMessages


class CrossroadsMessanger:

    WAITING_FOR_CHANGE_LIGHTS_NEED = "WAITING_FOR_CHANGE_LIGHTS_NEED"
    SEND_CFP = "SEND_CFP"
    WAITING_FOR_PROPOSALS = "WAITING_FOR_PROPOSALS"
    WAITING_FOR_INFORMS = "WAITING_FOR_INFORMS"

    # FIPA CONTRACT NET INTERACTION PROTOCOL... almost
    class NegotiatingProtocolInitiator(FSMBehaviour):

        async def on_start(self):
            self.add_state(name=CrossroadsMessanger.WAITING_FOR_CHANGE_LIGHTS_NEED, state=self.ChangeLightsNeededSetData(), initial=True)
            self.add_state(name=CrossroadsMessanger.SEND_CFP, state=self.SendCFP())
            self.add_state(name=CrossroadsMessanger.WAITING_FOR_PROPOSALS, state=self.WaitingForProposals())
            self.add_state(name=CrossroadsMessanger.WAITING_FOR_INFORMS,state=self.WaitingForInforms())
            self.add_transition(source=CrossroadsMessanger.WAITING_FOR_CHANGE_LIGHTS_NEED, dest=CrossroadsMessanger.SEND_CFP)
            self.add_transition(source=CrossroadsMessanger.SEND_CFP, dest=CrossroadsMessanger.WAITING_FOR_PROPOSALS)
            self.add_transition(source=CrossroadsMessanger.WAITING_FOR_PROPOSALS, dest=CrossroadsMessanger.WAITING_FOR_INFORMS)

        class ChangeLightsNeededSetData(State):
            async def run(self):
                # print("[{}] jestem w stanie SETDATA".format(self.agent.jid))

                # collecting data for request of changing lights
                AlgorithmFunctions.set_what_to_do_with_lights(self.agent)
                self.set_next_state(CrossroadsMessanger.SEND_CFP)

        class SendCFP(State):
            async def run(self):
                # print("[{}] jestem w stanie SEND CFP".format(self.agent.jid))

                # build request for changing lights => CFP message of Protocol
                for message in self.build_messages():
                    await self.send(message)
                self.set_next_state(CrossroadsMessanger.WAITING_FOR_PROPOSALS)

            def build_messages(self):
                messages = []
                for neighbour_jid in self.agent.neighbours_jid.values():
                    messages.append(CrossroadsMessages.build_cfp(neighbour_jid, self.agent))
                return messages

        class WaitingForProposals(State):
            async def run(self):
                # print("[{}] jestem w stanie WAITING PROPOSALS".format(self.agent.jid))

                proposals = {neighbour_jid: None for neighbour_jid in self.agent.neighbours_jid.values()}
                neigh_send_proposal_cnt = 0

                # collect proposals neighbours
                while neigh_send_proposal_cnt != len(self.agent.neighbours_jid):
                    # timeout set randomly to let agent collect answers
                    msg = await self.receive(timeout=5)
                    if msg and msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.PROPOSE:
                        # msg.sender is fucked up, so its easier to get sender jid via formating it to string than from dict
                        proposals["{}".format(msg.sender)] = msg
                        neigh_send_proposal_cnt += 1

                max_change_for = 0
                acc_proposal_jid = None

                # finding best proposal sender
                for neighbour_jid, proposal in proposals.items():
                    if proposal.get_metadata(messages_body_labels.can_you):
                        if max_change_for < proposal.get_metadata(messages_body_labels.change_by):
                            acc_proposal_jid = neighbour_jid

                # sending accept to best proposal sender and reject to the rest
                for neighbour_jid, proposal in proposals.items():
                    if neighbour_jid == acc_proposal_jid:
                        # TODO: NASTAWIC TU COS W AGENCIE, ABY WIEDZIAL O ILE SKROCIC I/LUB WYDLUZYC KONKRETNE SWIATLA
                        # kierunek nastaw zna (self.cfp[messages_body_labels.direction]), ale czas na wydluzenie/skrocenie przychodzi z proposalem
                        # jesli direction z cfp jest inny niz aktualny kierunek zielonego to odjac czas od pozostalego do zmiany swiatla
                        await self.send(CrossroadsMessages.build_cfp_accept_proposal(proposal))
                    else:
                        await self.send(CrossroadsMessages.build_cfp_rejected_proposal(proposal))

                self.set_next_state(CrossroadsMessanger.WAITING_FOR_INFORMS)

        class WaitingForInforms(State):
            async def run(self):
                # print("[{}] jestem w stanie WAITING INFORM".format(self.agent.jid))
                neigh_send_inform_cnt = 0

                # collect inform messages from all neighbours to finish protocol
                while neigh_send_inform_cnt != len(self.agent.neighbours_jid):
                    msg = await self.receive(timeout=5)
                    if msg and msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.INFORM:
                        neigh_send_inform_cnt += 1

                # print("[{}] SZKONCZYLEM PROTOKOL!!!!".format(self.agent.jid))

    class NegotiatingProtocolParticipant(CyclicBehaviour):
        async def run(self):
            reply = None
            msg = await self.receive()
            if msg:
                # if got CFP, create proposal to answear it
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.CFP:
                    reply = CrossroadsMessages.build_cfp_propose(participant=self.agent, received_cfp=msg)

                # if both ACCEPT (initiatior accept your proposal) or REJECT, send ok to end protocol
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.ACCEPT_PROPOSAL:
                    reply = CrossroadsMessages.build_cpf_inform(received_message=msg, ok=True)
                if msg.get_metadata(CrossroadsMessages.PERFORMATIVE) == CrossroadsMessages.REJECT_PROPOSAL:
                    reply = CrossroadsMessages.build_cpf_inform(received_message=msg, ok=False)
                if reply:
                    await self.send(reply)
