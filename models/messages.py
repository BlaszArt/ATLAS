import json

from spade.message import Message

from behaviours.functions import AlgorithmFunctions


# FIPA CONTRACT NET INTERACTION PROTOCOL... almost all message types to be used
class CrossroadsMessages:

    PERFORMATIVE = "performative"
    CFP = "cfp"
    PROPOSE = "propose"
    ACCEPT_PROPOSAL = "accept-proposal"
    REJECT_PROPOSAL = "reject-proposal"
    INFORM = "inform"

    @staticmethod
    def build_cfp(receiver, agent_sender):
        msg = Message(to=receiver)
        msg.thread = str(agent_sender.jid)
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE, CrossroadsMessages.CFP)
        # msg.body dont like dicts (but strings), so... every data needed set to metadata, cause it;s a dict...
        msg.body = None
        msg.body = json.dumps(agent_sender.cfp)

        return msg

    @staticmethod
    def build_cfp_propose(participant, received_cfp):
        msg = received_cfp.make_reply()
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE,  CrossroadsMessages.PROPOSE)
        msg.body = None
        participant_proposal = AlgorithmFunctions.make_participant_proposal(participant, json.loads(received_cfp.body))
        msg.body = json.dumps(participant_proposal)
        print('[{}] MADE PROPOSAL for {}: {}'.format(participant.jid, msg.to, msg))

        return msg

    @staticmethod
    def build_cfp_accept_proposal(received_proposal):
        msg = received_proposal.make_reply()
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE,  CrossroadsMessages.ACCEPT_PROPOSAL)
        msg.body = 'ACCEPTED'
        print("[{}] posylam do [{}] ACCEPT".format(received_proposal.to, msg.to))
        return msg

    @staticmethod
    def build_cfp_rejected_proposal(received_proposal):
        msg = received_proposal.make_reply()
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE,  CrossroadsMessages.REJECT_PROPOSAL)
        msg.body = 'REJECTED'
        print("[{}] posylam do [{}] REJECT".format(received_proposal.to, msg.to))
        return msg

    @staticmethod
    def build_cpf_inform(received_message, ok):
        msg = received_message.make_reply()
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE, CrossroadsMessages.INFORM)
        msg.body = str(ok)
        print("[{}] posylam do [{}] INFORM".format(received_message.to, msg.to))
        return msg

