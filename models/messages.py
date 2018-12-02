from spade.message import Message

#todo trzeba dodac thread'y wiadomosciom by ogarnąć co od kogo przyszlo - np. nazwa threada jako jid agenta ktory chce zmienic
class CrossroadsMessages:
    PERFORMATIVE = "performative"
    CFP = "cfp"
    PROPOSE = "propose"
    ACCEPT_PROPOSAL = "accept-proposal"
    REJECT_PROPOSAL = "reject-proposal"
    INFORM = "inform"
    
    cars = "cars"
    lights = "lights"
    direction = "direction"
    to_change = "to_change?"
    when_in_sec = 'when_in_sec'
    can_you = "can_you?"
    ok = "ok"

    @staticmethod
    def build_cfp(receiver,sender, direction, to_change, in_sec):
        msg = Message(to=receiver)
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE, CrossroadsMessages.CFP)
        msg_body = sender.crossroad.get_status()
        msg_body[CrossroadsMessages.direction] = direction
        msg_body[CrossroadsMessages.to_change] = to_change
        msg_body[CrossroadsMessages.when_in_sec] = in_sec
        msg.body = msg_body
        return msg

    @staticmethod
    def build_cfp_propose(receiver ,can_you, in_sec):
        msg = Message(to=receiver)
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE,  CrossroadsMessages.PROPOSE)
        msg_body = {CrossroadsMessages.can_you: can_you,
                    CrossroadsMessages.when_in_sec: in_sec}
        msg.body = msg_body
        return msg

    @staticmethod
    def build_cfp_accept_proposal(receiver,can_you, in_sec):
        msg = Message(to=receiver)
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE,  CrossroadsMessages.ACCEPT_PROPOSAL)
        msg_body = {CrossroadsMessages.can_you: can_you,
                    CrossroadsMessages.when_in_sec: in_sec}
        msg.body = msg_body
        return msg

    @staticmethod
    def build_cpf_inform(receiver ,ok):
        msg = Message(to=receiver)
        msg.set_metadata(CrossroadsMessages.PERFORMATIVE, CrossroadsMessages.INFORM)
        msg_body = {CrossroadsMessages.ok:ok}
        msg.body = msg_body
        return msg

