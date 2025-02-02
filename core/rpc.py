import inspect
import json
import socket
from threading import Thread
import logging

SIZE = 1024
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RPCServer:

    def __init__(self, host: str = '0.0.0.0', port: int = 8080) -> None:
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    def help(self) -> None:
        logging.info('REGISTERED METHODS:')
        for method in self._methods.items():
            logging.info('\t', method)

    '''

        registerFunction: pass a method to register all its methods and attributes so they can be used by the client via rpcs
            Arguments:
            instance -> a class object
    '''

    def registerMethod(self, function) -> None:
        try:
            self._methods.update({function.__name__: function})
        except:
            raise Exception('A non method object has been passed into RPCServer.registerMethod(self, function)')

    '''
        registerInstance: pass a instance of a class to register all its methods and attributes so they can be used by the client via rpcs
            Arguments:
            instance -> a class object
    '''

    def registerInstance(self, instance=None) -> None:
        try:
            # Regestring the instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'):
                    self._methods.update({functionName: function})
        except:
            raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')

    '''
        handle: pass client connection and it's address to perform requests between client and server (recorded fucntions or) 
        Arguments:
        client -> 
    '''

    def __handle__(self, client: socket.socket, address: tuple):
        logging.info(f'Managing requests from {address}.')
        while True:
            try:
                decode = client.recv(SIZE).decode()
                logging.info(f"Received request: {decode}")
                if decode == 'test':
                    client.sendall("success".encode())
                    continue
                functionName, args, kwargs = json.loads(decode)
            except:
                logging.exception(f"While handling request: {decode}")
                logging.info(f'! Client {address} disconnected.')
                break
            # Showing request Type
            logging.info(f'> {address} : {functionName}({args})')

            try:
                response = self._methods[functionName](*args, **kwargs)
            except Exception as e:
                # Send back exeption if function called by client is not registred
                client.sendall(json.dumps(str(e)).encode())
            else:
                client.sendall(json.dumps(response).encode())

        logging.info(f'Completed request from {address}.')
        client.close()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()

            logging.info(f'+ Server {self.address} running')
            while True:
                try:
                    client, address = sock.accept()

                    Thread(target=self.__handle__, args=[client, address]).start()

                except KeyboardInterrupt:
                    logging.info(f'- Server {self.address} interrupted')
                    break


class RPCClient:
    def __init__(self, host: str = 'localhost', port: int = 8080) -> None:
        self.__sock = None
        self.__address = (host, port)

    def is_connected(self):
        try:
            logging.info("Checking connection")
            self.__sock.sendall(b'test')
            success = 'success' == self.__sock.recv(SIZE).decode()
            logging.info(f"Connection status: {success}")
            return success
        except:
            return False

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect(self.__address)
        except EOFError as e:
            logging.info(e)
            raise Exception('Client was not able to connect.')

    def disconnect(self):
        try:
            self.__sock.close()
        except:
            pass

    def __getattr__(self, __name: str):
        def execute(*args, **kwargs):
            logger.info(f"Sending {json.dumps((__name, args, kwargs)).encode()}")
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())
            decode = self.__sock.recv(SIZE).decode()
            logger.info(f"Received {decode}")
            response = json.loads(decode)

            return response

        return execute

    def __del__(self):
        try:
            self.__sock.close()
        except:
            pass
