from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from functools import partial
from kivy.clock import Clock
from kivy.app import App
import webbrowser

Window.clearcolor = (1, 1, 1, 1)


class NumPadRoot(BoxLayout):
	login = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(NumPadRoot, self).__init__(**kwargs)
		self.stages = {"prep_list": {"drugs": 0, "ultrasound": 0, "stimulator": 0, "patient": 0, "gloved": 0},
						"stop_list": {"reconfirm": 0, "ask_patient": 0, "appropriate": 0}}
		self.screen_list = []

	def change_screen(self, next_screen, *args):
		if self.ids.kivy_screen_manager.current not in self.screen_list:
			self.screen_list.append(self.ids.kivy_screen_manager.current)

		self.ids.kivy_screen_manager.current = next_screen

	def on_back_button(self):
		if self.screen_list:
			self.ids.kivy_screen_manager.current = self.screen_list.pop()
			return True
		return False

	def on_checkbox_active(self, stage, checkbox_instance, is_active):
		if is_active:
			self.stages[stage][checkbox_instance] = 1
		else:
			self.stages[stage][checkbox_instance] = 0

	def on_next_stage(self, instance, current_stage, next_stage):
		tests = [i for i in self.stages[current_stage].values()]
		if all(tests):
			instance.text = "[b]Tests Completed[/b]"
			instance.background_color = (0, 1, 0, 1)
			Clock.schedule_once(partial(self.change_screen, next_stage), 0.3)
		else:
			instance.text = "[b]Complete all tests and try again[/b]"

	def on_unlock(self, instance):
		instance.text = "[b]Box Unlocked[/b]"
		instance.background_color = (0, 1, 0, 1)


class NumPadApp(App):
	def __init__(self, **kwargs):
		super(NumPadApp, self).__init__(**kwargs)
		Window.bind(on_keyboard=self.on_back_button)

	def build(self):
		return NumPadRoot()

	def on_back_button(self, window, key, _):
		if key == 27:
			print(window)
			return self.root.on_back_button()

	def get_text(self):
		return ("Developers: [b]Bharat[/b] and [b]Yogen[/b]"
				"Supervisor: [b]Dr. Stefan Poslad[/b]"
				"Supporters: [b]Whipps Cross Hospital[/b]"
				"[ref=contact]Contact us[/ref]")

	def on_ref_press(self, _, ref):
		_dict = {
			"contact": "https://www.google.com/"
		}

		webbrowser.open(_dict[ref])


class LoginScreen(Screen):
	def __init__(self, *args, **kwargs):
		super(LoginScreen, self).__init__(*args, **kwargs)

	def check_pin(self, pin):
		if pin == '0000':
			return True
		else:
			return False


class NumPad(GridLayout):
	def __init__(self, *args, **kwargs):
		super(NumPad, self).__init__(*args, **kwargs)
		self.cols = 3
		self.spacing = 10
		self.create_buttons()
		self.input = ""

	def create_buttons(self):
		_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "*", "GO!"]
		for num in _list:
			self.add_widget(Button(text=str(num), on_release=self.on_btn_press, markup=True, font_size=20))

	def on_btn_press(self, btn):
		login = App.get_running_app().root.ids.login
		input_pin = login.input_pin
		if btn.text.isdigit():
			self.input += btn.text
			input_pin.text += "*"
		if btn.text == "GO!" and input_pin.text != "":
			check = self.input[-4:]
			print(login.check_pin(check))
			input_pin.text = ""
			self.input = ""
			App.get_running_app().root.change_screen("prep")

	def clear_button(self):
		self.input = ""
		login = App.get_running_app().root.ids.login
		input_pin = login.input_pin
		input_pin.text = ""


class ChecklistScreen(Screen):
	def __init__(self, *args, **kwargs):
		super(ChecklistScreen, self).__init__(*args, **kwargs)
		self.check1 = self.check2 = False

	def released_1(self, obj):
		self.check1 = True
		obj.background_color = (0, 1, 0, 1)

	def released_2(self, obj):
		self.check2 = True
		obj.background_color = (0, 1, 0, 1)

	def unlock_box(self):
		checklist = App.get_running_app().root.ids.checklist
		label = checklist.checklist_label
		if all([self.check1, self.check2]):
			label.text = "Box Unlocked"
		else:
			print('Tests Incomplete')


class StockScreen(Screen):
	def __init__(self, *args, **kwargs):
		super(StockScreen, self).__init__(*args, **kwargs)

	def get_text(self):
		return "Stocks"

	def print_stocks(self):
		stocks = App.get_running_app().root.ids.stocks
		label = stocks.stock_print
		send_data = {'SENS': 5, 'TIME': 2}
		print("Sending")
		print_data = ""
		for key, value in send_data.items():
			# ser.write(str.encode(key))
			print("Receiving")
			line = ""
			for _ in range(value + 1):
				# line = ser.readline().decode('utf-8').rstrip()
				line = "test"
			print_data = print_data + line + "\n"
		label.text = print_data


if __name__ == '__main__':
	NumPadApp().run()
