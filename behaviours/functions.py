import operator

from models import messages_body_labels

# INITIATOR - THIS ONE WHO SEND CFP
# PARTICIPANT - ANSWEARS CFP
class AlgorithmFunctions:

    #       abs(max(cars[NS]) - max(cars[WE])) = time
    #       max(cars[NS]) > max(cars[WE]) => NS, == bz, else WE
    #       jesli wygrywa kierunek aktualnie sie swiecacy to przedluzamy, jesli przeciwny to skracamy aktualne swiatla o time
    #       na 0 zostaje jak jest
    @staticmethod
    def set_what_to_do_with_lights(agent):
        actual_lights_direction = agent.get_actual_green_lights_direction()

        # getting data about how to change time of actual light state
        change_time_by = AlgorithmFunctions.cars_to_time(
            abs(agent.directions_max_cars['NS'] - agent.directions_max_cars['EW']))
        agent.cfp[messages_body_labels.change_by] = change_time_by

        # if both directions got the same amount of cars - do nothing
        if change_time_by == 0:
            agent.cfp[messages_body_labels.to_change] = False
            agent.cfp[messages_body_labels.direction] = actual_lights_direction

        # if is difference, try to change lights quicker if busiest direction is now with red light
        # or make lights last longer if busiest got green light right now
        else:
            busiest_direction = max(agent.directions_max_cars.items(), key=operator.itemgetter(1))[0]
            if busiest_direction != actual_lights_direction:
                agent.cfp[messages_body_labels.to_change] = True
                agent.cfp[messages_body_labels.direction] = busiest_direction
            else:
                agent.cfp[messages_body_labels.to_change] = False
                agent.cfp[messages_body_labels.direction] = actual_lights_direction

        # print("[{}] ustalilem CFP: {} / {} / {}".format(agent.jid, agent.cfp[messages_body_labels.direction],
        #                                                 agent.cfp[messages_body_labels.to_change],
        #                                                 agent.cfp[messages_body_labels.change_by]))


    # jesli potencjalny nowy kierunek swiatel partycypanta jest zgodny z przyszlym inicjatora, przyjmij cfp odsylajac propozycje z tymi samymi wartosciami
    # jesli sie nie zgadza, a czas zmiany u partycypanta jest wyzszy niz suma aut, ktore moga nadjechac od sasiada + oczekujacych u partycypanta
    #  to odeslij czas partycypanta + 1 (bo chcemy opóźnić)
    @staticmethod
    def make_participant_proposal(participant, cfp_message):
        participant_proposal = {messages_body_labels.can_you: None,
                                messages_body_labels.change_by: None}

        # getting whats expected by initiator - crossroad want to change lights
        init_change_direction = cfp_message.get_metadata(messages_body_labels.direction)
        init_change_for = cfp_message.get_metadata(messages_body_labels.change_by)

        # getting data of potential changes on participant crossroad
        # print('[{}] EW: {}'.format(participant.jid, participant.directions_max_cars['EW'])) # close look at it needed - sometimes gets exception on EW value...
        part_potential_change_time = AlgorithmFunctions.cars_to_time(
            abs(participant.directions_max_cars['NS'] - participant.directions_max_cars['EW']))
        part_potential_change_dir = max(participant.directions_max_cars.items(), key=operator.itemgetter(1))[0]

        #start of analyzing and making proposal
        if (init_change_direction != part_potential_change_dir and
                init_change_for + participant.directions_max_cars[part_potential_change_dir] < part_potential_change_time):

            participant_proposal[messages_body_labels.can_you] = True
            participant_proposal[messages_body_labels.change_by] = part_potential_change_time + 1
        else:
            participant_proposal[messages_body_labels.can_you] = True
            participant_proposal[messages_body_labels.change_by] = init_change_for

        # print("[{}] ustalilem PROPOSAL: {} / {}".format(participant.jid,
        #                                                 participant_proposal[messages_body_labels.can_you],
        #                                                 participant_proposal[messages_body_labels.change_by]))

        return participant_proposal

    # Cars (no.) = time needed (in sec)
    @staticmethod
    def cars_to_time(cars_counter):
        return cars_counter
