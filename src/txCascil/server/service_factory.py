import txCascil.packings  # @UnusedImport
from txCascil.registry_manager import RegistryManager
from txCascil.server.authentication_controller_factory import AuthenticationControllerFactory
from txCascil.server.client_controller_factory import ClientControllerFactory
from txCascil.server.protocol_factory import ProtocolFactory
from txCascil.server.service import Service
import txCascil.transports  # @UnusedImport


class ServerServiceFactory(object):
    def __init__(self):
        self._transports = {}
        self._packings = {}

        for transport_registration in RegistryManager.get_registrations('transport'):
            transport_name = transport_registration.args[0]
            transport_class = transport_registration.registered_object
            self._transports[transport_name] = transport_class

        for packing_registration in RegistryManager.get_registrations('packing'):
            packing_name = packing_registration.args[0]
            packing_class = packing_registration.registered_object
            self._packings[packing_name] = packing_class

    def build_service(self, context, config, message_handlers, permission_resolver, event_subscription_fulfiller):
        transport_name = config['transport']
        packing_name = config['packing']

        TransportProtocol = self._transports[transport_name]
        packing = self._packings[packing_name]

        authentication = config['authentication']

        authentication_controller_factory = AuthenticationControllerFactory(authentication)

        client_controller_factory = ClientControllerFactory(context, message_handlers, permission_resolver, event_subscription_fulfiller)

        factory = ProtocolFactory(TransportProtocol, packing, client_controller_factory, authentication_controller_factory)

        interface = config['interface']
        port = config['port']

        return Service(interface, port, factory)
