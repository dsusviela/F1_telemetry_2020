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
    self.session_names_by_index = {}
    self.session_information = {}

  def update_from_packet(self, packet):
    data = unpack_udp_packet(packet)
    if data.header.packetId == PacketID.SESSION:
      self.session_information["trackLength"] = data.trackLength
    elif data.header.packetId == PacketID.PARTICIPANTS:
      for index, participant in enumerate(data.participants):
        self.session_names_by_index[index] = participant.name.decode(encoding='UTF-8',errors='strict')
        if participant.aiControlled == 0:
          self.session_names_by_index[index] += str(participant.raceNumber)
          print(participant)
    elif data.header.packetId == PacketID.LAP_DATA:
      session_data_by_index = {}
      for index, participant in enumerate(data.lapData):
        session_data_by_index[index] = self._parse_participant_data(participant, index)

      for index, driver_data in session_data_by_index.items():
        if driver_data["position"] != 0:
          self.session_qualyfication[driver_data["position"]] = driver_data

  def _parse_participant_data(self, participant, index):
    print(self._lastThreeLapTimes(participant, index))

    name = self.session_names_by_index[index] if index in self.session_names_by_index else "driver"

    return {
      "lastLapTime": participant.lastLapTime,
      "position": participant.carPosition,
      "name": name,
      "penalties": participant.penalties,
      "lastThreeLapTimes": self._lastThreeLapTimes(participant, index)
    }
  
  def _lastThreeLapTimes(self, participant, index):
    if "trackLength" not in self.session_information:
      return [0,0,0]
    
    if participant.totalDistance <= self.session_information["trackLength"]:
      return [0,0,0]
    
    if participant.carPosition in self.session_qualyfication and "lastThreeLapTimes" in self.session_qualyfication[participant.carPosition]:
      arrayIndex = (int(participant.totalDistance // self.session_information["trackLength"]) % 3) - 1
      self.session_qualyfication[participant.carPosition]["lastThreeLapTimes"][arrayIndex] = participant.lastLapTime
      return self.session_qualyfication[participant.carPosition]["lastThreeLapTimes"]
    else:
      return [participant.lastLapTime, 0, 0]

