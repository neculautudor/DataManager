from tendo.singleton import SingleInstance
from frontend.components.Root.frontend_QT import Window, app


def run_app():
		me = SingleInstance()
		window = Window()
		window.show()
		# window.adjustSize()
		app.exec()

if __name__ == '__main__':
	run_app()