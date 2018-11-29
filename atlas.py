from agents import crossroad_agent
import time

if __name__ == '__main__':
    dummy = crossroad_agent.CrossroadAgent("agent2@jabbim.pl", "agent2")
    dummy.start()

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            dummy.stop()
            break
