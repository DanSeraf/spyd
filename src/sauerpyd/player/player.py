from sauerpyd.player.player_network_base import PlayerNetworkBase
from sauerpyd.player.player_state import PlayerState
from sauerpyd.protocol import swh
from sauerpyd.server_message_formatter import smf


class Player(PlayerNetworkBase):
    def __init__(self, client, playernum, name, playermodel):
        PlayerNetworkBase.__init__(self, client)
        self._pn = playernum
        self.name = name
        self.playermodel = playermodel
        self._team = None
        self._isai = False
        
        self._state = PlayerState()
        
    @property
    def cn(self):
        return self._pn
        
    @property
    def pn(self):
        return self._pn
        
    @property
    def state(self):
        return self._state
        
    @property
    def isai(self):
        return self._isai
        
    @property
    def room(self):
        return self.client.room
        
    @property
    def team(self):
        if self._state.is_spectator:
            return None
        return self._team
    
    @team.setter
    def team(self, team):
        self._team = team

    @property
    def shares_name(self):
        return self.room.is_name_duplicate(self.name)

    def __format__(self, format_spec):
        if self.shares_name or self.isai:
            fmt = "{name#player.name} {pn#player.pn}"
        else:
            fmt = "{name#player.name}"
            
        return smf.format(fmt, player=self)
            
    def on_respawn(self, lifesequence, gunselect):
        self.state.on_respawn(lifesequence, gunselect)
        
    def write_state(self, room_positions, room_messages):
        if self.state.position is not None:
            room_positions.write(self.state.position)

        if not self.state.messages.empty():
            swh.put_clientdata(room_messages, self, self.state.messages)