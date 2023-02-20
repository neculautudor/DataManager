from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QComboBox, QVBoxLayout, QDialog, QDialogButtonBox, QLabel


def button(name, action):
	btn = QPushButton(name)
	btn.clicked.connect(action)
	return btn

class Button(QPushButton):
	def __init__(self, name, action, icon):
		super().__init__()
		self.setText(name)
		self.action = action
		if icon:
			self.setIcon(QIcon(icon))
		self.clicked.connect(self.action)

class SelectableButton(QPushButton):
	def __init__(self, name, action):
		super().__init__()
		self.setText(name)
		self.selected = False
		self.action = action
		self.clicked.connect(self.on_click)

	def on_click(self):
		self.select_or_deselect()
		self.action()

	def select_or_deselect(self):
		self.selected = not self.selected
		self.setStyleSheet(
		 'QPushButton {background-color: #A3C1DA;}' if self.selected == True else
		 'QPushButton {background-color: #f0f0f0; color: black;}'
		)


class CustomDialog(QDialog):
	def __init__(self, window_title, message, with_cancel):
		super().__init__()

		self.setWindowTitle(window_title)

		if with_cancel:
			QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
		else:
			QBtn = QDialogButtonBox.StandardButton.Ok

		self.buttonBox = QDialogButtonBox(QBtn)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

		self.layout = QVBoxLayout()
		message = QLabel(message)
		self.layout.addWidget(message)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)


class SelectDelete(QComboBox):
	def __init__(self, options):
		super().__init__()
		self.addItems(options)
	def reset(self, new_options):
		self.clear()
		self.addItems(new_options)


class PopupWindow(CustomDialog):
	def __init__(self, title, description, action, with_cancel):
		super().__init__(
			window_title=title,
			message=description,
			with_cancel=with_cancel
		)
		if self.exec():
			if action:
				action()














