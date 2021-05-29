from lib.data_manager import DataManager
import threading
from lib.window import Window
from lib.network_manager import NetworkManager

mutex = threading.Semaphore(1)

window = Window()
network_manager = NetworkManager(mutex)
data_manager = DataManager()

network_thread = threading.Thread(target=network_manager.receive_packet, daemon=True)
network_thread.start()

while True:
  event, _values = window.render()
  if event is None or event == 'Exit':
    break

  mutex.acquire()
  window.update_session_layout(data_manager.session_qualyfication)
  mutex.release()

window.close()
