from xmlrpc.server import SimpleXMLRPCServer
from django.http import HttpResponse
from fasteners.models import Fastener
import threading

class MechanicalToolboxRPC:
    @staticmethod
    def get_fastener_details(fastener_id):
        try:
            fastener = Fastener.objects.get(pk=fastener_id)
            return {
                'id': fastener.id,
                'type': fastener.type,
                'diameter': fastener.diameter,
                'length': fastener.length,
                'material': fastener.material,
                'strength_class': fastener.strength_class
            }
        except Fastener.DoesNotExist:
            return {'error': 'Fastener not found'}
    
    @staticmethod
    def calculate_preload(fastener_id, friction_coefficient):
        # Implement calculation logic
        pass

def start_xmlrpc_server():
    server = SimpleXMLRPCServer(('localhost', 8001), allow_none=True)
    server.register_instance(MechanicalToolboxRPC())
    server.serve_forever()

# Start the XML-RPC server in a separate thread
threading.Thread(target=start_xmlrpc_server, daemon=True).start()