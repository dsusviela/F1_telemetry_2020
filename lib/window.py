import PySimpleGUI as sg
import datetime

class Window:
  def __init__(self):
    my_new_theme = {'BACKGROUND': '#15151e',
                'TEXT': '#f7f4f1',
                'INPUT': '#fff8c5',
                'TEXT_INPUT': '#fff8c5',
                'SCROLL': '#38383f',
                'BUTTON': ('#ee0000', '#ee0000'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}
    sg.theme_add_new('MyNewTheme', my_new_theme)
    sg.theme('My New Theme')
    self.layout = self.__create_initial_layout()
    self.main_window = sg.Window(title="F1 TELEMETRY APP - Cucu productions", layout=[self.layout], font="Helvetica 18")

  def render(self):
    return self.main_window.read(timeout=10)

  def close(self):
    return self.main_window.close()

  def update_session_layout(self, session_qualyfication):
    for position in session_qualyfication.keys():
      last_lap_time = session_qualyfication[position]["lastLapTime"]
      driver_name = session_qualyfication[position]["name"]
      self.main_window[f"-DRIVER-POS#{position}-"].Update(driver_name)
      self.main_window[f"-DRIVER-TIME#{position}-"].Update(self.__parse_time(last_lap_time))

  def __parse_time(self, time):
    return str(datetime.timedelta(seconds=time))[:-3]

  def __create_initial_layout(self):
    drivers = []
    times = []
    for i in range(0, 22):
      drivers += [f"driver{i}"]
      times += ['00:00:00.000']

    driver_names_layout = []
    for index, driver in enumerate(drivers):
      driver_text = sg.Text(driver, auto_size_text=False, key=f"-DRIVER-POS#{index + 1}-")
      driver_time = sg.Text(times[index], auto_size_text=False, key=f"-DRIVER-TIME#{index + 1}-")
      driver_names_layout += [[driver_text, driver_time]]
    return driver_names_layout
