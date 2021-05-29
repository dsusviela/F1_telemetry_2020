import PySimpleGUI as sg
import datetime
from lib.constants import AI_DRIVERS_IDS_AND_NAMES

class Window:
  def __init__(self):
    drivers = []
    times = []
    for i in range(0, 22):
      drivers += [f"driver{i}"]
      times += ['00:00:00.000']

    self.layout = self.__create_initial_layout(drivers, times)
    self.main_window = sg.Window(title="F1 TELEMETRY APP - Cucu productions", layout=[self.layout], font="Helvetica 18")

  def render(self):
    return self.main_window.read(timeout=10)

  def close(self):
    return self.main_window.close()

  def update_session_layout(self, session_qualyfication):
    for position in session_qualyfication.keys():
      last_lap_time = session_qualyfication[position]["lastLapTime"]
      driver_id = session_qualyfication[position]["driverId"]
      driver_name = AI_DRIVERS_IDS_AND_NAMES[int(driver_id)]
      self.main_window[f"-DRIVER-POS#{position}-"].Update(driver_name)
      self.main_window[f"-DRIVER-TIME#{position}-"].Update(self.__parse_time(last_lap_time))

  def __parse_time(self, time):
    return str(datetime.timedelta(seconds=time))[:-3]

  def __create_initial_layout(self, drivers, times):
    driver_names_layout = []
    for index, driver in enumerate(drivers):
      driver_text = sg.Text(driver, auto_size_text=False, key=f"-DRIVER-POS#{index + 1}-")
      driver_time = sg.Text(times[index], auto_size_text=False, key=f"-DRIVER-TIME#{index + 1}-")
      driver_names_layout += [[driver_text, driver_time]]
    return driver_names_layout
