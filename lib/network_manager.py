import socket
from lib.data_manager import DataManager

class NetworkManager:
  def __init__(self, mutex):
    self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    self.socket.bind(('', 20777))
    self.data_manager = DataManager()
    self.mutex = mutex

  def receive_packet(self):
    while True:
      udp_packet = self.socket.recv(2048)

      self.mutex.acquire()
      self.data_manager.update_from_packet(udp_packet)
      self.mutex.release()

