from spyd.registry_manager import register


@register('client_message_handler')
class TrydropflagHandler(object):
    message_type = 'N_TRYDROPFLAG'

    @staticmethod
    def handle(client, room, message):
        player = client.get_player(message['aiclientnum'])
        room.handle_player_event('try_drop_flag', player)
