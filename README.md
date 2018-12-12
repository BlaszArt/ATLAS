# atlas
A Traffic Lights Agent System

Wiadomosci dla protokolu:

CFP:
cars: {kierunek: liczba aut}
lights: {kierunek: czy zapalone}
direction: kierunek zmiany lub zostawienia swiatel
to_change?: czy chce zmienic: True - chce zmienic, False - chce przedluzyc aktualne
when_in_sec: o ile chce to zrobic

PROPOSE:
can_you: True - mozesz, False - nie
when_in_sec: o ile mozesz

ACCEPT-PROPOSAL - to samo co Propose, ale na bank na True
REJECT-PROPOSAL - -||- ale z False

INFORM - ok: True, potwierdzenie na sam koniec, nieistotne



================= LINUX ================================
1. Instalacja: sudo apt install prosody
2. Podmienić plik /etc/prosody/prosody.cfg.lua na odpowiadający w folderze utils projektu
3. Restart serwera prosody komendą: sudo prosodyctl restart
4. Gotowe! W razie problemów z rejestracją agentów można uruchomić skrypty zamieszone w folderze utils.

!! Format jid agentów: xx@localhost !!!!!