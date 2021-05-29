from f1_2020_telemetry.packets import unpack_udp_packet
from f1_2020_telemetry.packets import PacketID

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DataManager(metaclass=Singleton):
  def __init__(self):
    self.session_qualyfication = {}
    self.session_ids_by_index = {}

  def update_from_packet(self, packet):
    data = unpack_udp_packet(packet)
    if data.header.packetId == PacketID.PARTICIPANTS:
      for index, participant in enumerate(data.participants):
        self.session_ids_by_index[index] = participant.driverId
    elif data.header.packetId == PacketID.LAP_DATA:
      session_data_by_index = {}
      for index, participant in enumerate(data.lapData):
        session_data_by_index[index] = { "lastLapTime": participant.lastLapTime, "position": participant.carPosition, "driverId": self.session_ids_by_index[index] }

      for index, driver_data in session_data_by_index.items():
        if driver_data["position"] != 0:
          self.session_qualyfication[driver_data["position"]] = driver_data