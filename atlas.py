# Aktualne skrzyzowanie - numery w srodku to numery agentow - ca1 = crossroad_agent_1 itd.
# nastawione szybkosci sa takie, ze oba skrzyzowania po lewej szybciej przepuszczaja i generuja auta niz te po prawo
#
#    N        N
#    |        |
#-W--1--E--W--2--E
#    |        |
#    S        S
#    |        |
#-W--3--E--W--4--E
#    |        |
#    S        S


from agents import crossroad_agent, manager_agent
import time

if __name__ == '__main__':
    ca1 = crossroad_agent.CrossroadAgent(jid="ca1@jabbim.pl", password="crossroad1", manager_jid="ma1@jabbim.pl", cars_speed=2)
    ca2 = crossroad_agent.CrossroadAgent(jid="ca2@jabbim.pl", password="crossroad2", manager_jid="ma1@jabbim.pl", cars_speed=1)
    ca3 = crossroad_agent.CrossroadAgent(jid="ca3@jabbim.pl", password="crossroad3", manager_jid="ma1@jabbim.pl", cars_speed=2)
    ca4 = crossroad_agent.CrossroadAgent(jid="ca4@jabbim.pl", password="crossroad4", manager_jid="ma1@jabbim.pl", cars_speed=1)
    ma1 = manager_agent.ManagerAgent("ma1@jabbim.pl", "manageragent1", topology='examples/topology_example.json')
    ca1.start(neighbours={'S': ca4, 'W': ca1})
    ca2.start(neighbours={'S': ca4, 'W': ca1})
    ca3.start(neighbours={'N': ca1, 'E': ca4})
    ca4.start(neighbours={'N': ca2, 'W': ca3})
    ma1.start()

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ca1.stop()
            ca2.stop()
            ca3.stop()
            ca4.stop()
            ma1.stop()
            break
