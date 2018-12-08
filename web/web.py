import webbrowser

class Web:
    @staticmethod
    def generate_web(agents, open_tab=False):
        for n, agent in enumerate(agents):
            agent.web.start(hostname="127.0.0.1", port=n + 10000)

            if open_tab:
                webbrowser.open_new_tab(f"http://127.0.0.1:{n+10000}/spade")
