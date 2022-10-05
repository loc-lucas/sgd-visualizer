import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QWidget, QHBoxLayout, \
    QVBoxLayout, QListWidget, QComboBox
import glfw

from libs.window import Window
from math_util.equation_parser import EquationParser
from math_util.sgd import SGDOptimizer
from objects.ball.ball import Ball
from objects.surface.parametricsurface import ParametricSurface

colors = {
    'yellow': 0,
    'black': 1,
    'purple': 2,
    'white': 3,
    'cyan': 4
}


# Subclass QMainWindow to customize your application's main window
class BallWindow(QWidget):
    def __init__(self, ball_data, mode, delete_callback, save_callback):
        super().__init__()
        self.setWindowTitle("Ball Property")
        layout = QVBoxLayout()
        self.save_callback = save_callback
        # name
        name_label = QLabel("Name")
        name_layout = QHBoxLayout()
        name_layout.addWidget(name_label)
        self.name_edit = QLineEdit(ball_data['name'])
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        # color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color"))
        self.color_cb = QComboBox()
        for key in colors:
            self.color_cb.addItem(key)
        self.color_cb.setCurrentIndex(colors[ball_data['color']])
        color_layout.addWidget(self.color_cb)
        layout.addLayout(color_layout)
        # Start pos
        layout.addWidget(QLabel('Start position'))
        # start x
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel())
        x_layout.addWidget(QLabel('X'))
        self.x_edit = QLineEdit(str(ball_data['start_x']))
        x_layout.addWidget(self.x_edit)
        layout.addLayout(x_layout)
        # start y
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel())
        y_layout.addWidget(QLabel('Y'))
        self.y_edit = QLineEdit(str(ball_data['start_y']))
        y_layout.addWidget(self.y_edit)
        layout.addLayout(y_layout)
        # learn rate
        learn_rate_layout = QHBoxLayout()
        learn_rate_layout.addWidget(QLabel('Learning rate'))
        self.learn_rate_edit = QLineEdit(str(ball_data['learn_rate']))
        learn_rate_layout.addWidget(self.learn_rate_edit)
        layout.addLayout(learn_rate_layout)
        # Momentum
        momentum_layout = QHBoxLayout()
        momentum_layout.addWidget(QLabel('Momentum'))
        self.momentum_edit = QLineEdit(str(ball_data['momentum']))
        momentum_layout.addWidget(self.momentum_edit)
        layout.addLayout(momentum_layout)
        # max iteration
        max_iter_layout = QHBoxLayout()
        max_iter_layout.addWidget(QLabel('Max iteration'))
        self.max_iter_edit = QLineEdit(str(ball_data['max_iter']))
        max_iter_layout.addWidget(self.max_iter_edit)
        layout.addLayout(max_iter_layout)
        # tolerance
        tolerance_layout = QHBoxLayout()
        tolerance_layout.addWidget(QLabel('Tolerance'))
        self.tol_edit = QLineEdit(str(ball_data['tolerance']))
        tolerance_layout.addWidget(self.tol_edit)
        layout.addLayout(tolerance_layout)
        # Buttons
        button_layout = QHBoxLayout()
        self.delete_btn = QPushButton('Delete' if mode == 'edit' else 'Cancel')
        self.delete_btn.clicked.connect(delete_callback)
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(self.save)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save(self):
        name = self.name_edit.text(),
        try:
            name = name[0]
        except:
            pass
        color = self.color_cb.currentText()
        start_x = self.x_edit.text()
        start_y = self.y_edit.text()
        learn_rate = self.learn_rate_edit.text()
        tolerance = self.tol_edit.text()
        max_iter = self.max_iter_edit.text()
        momentum = self.momentum_edit.text()
        if name == '':
            return
        if color == '':
            return
        if start_x == '':
            return
        if start_y == '':
            return
        if learn_rate == '':
            return
        if tolerance == '':
            return
        if max_iter == '':
            return
        if momentum == '':
            return
        ball = {
            'name': name,
            'color': color,
            'start_x': float(start_x),
            'start_y': float(start_y),
            'learn_rate': float(learn_rate),
            'tolerance': float(tolerance),
            'max_iter': float(max_iter),
            'momentum': float(momentum)
        }
        self.save_callback(ball)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ball_window = None
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle("My App")

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Expression:')
        main_layout.addWidget(self.nameLabel)
        self.expr = QLineEdit(self)
        # self.expr.move(100, 20)
        # self.expr.resize(200, 32)
        main_layout.addWidget(self.expr)
        # self.nameLabel.move(20, 20)

        # Balls
        ball_layout = QHBoxLayout()
        ball_label_widget = QWidget()
        self.ballLabel = QLabel(self)
        self.ballLabel.setText('Balls')
        self.add_ball_button = QPushButton("Add")
        ball_layout.addWidget(self.ballLabel)
        ball_layout.addWidget(self.add_ball_button)
        ball_label_widget.setLayout(ball_layout)
        self.add_ball_button.clicked.connect(self.add_ball)
        main_layout.addWidget(ball_label_widget)
        # list balls
        self.list_balls_data = []
        self.list_balls_widget = QListWidget()

        self.list_balls_widget.doubleClicked.connect(self.get_ball)
        main_layout.addWidget(self.list_balls_widget)

        # Generate button
        button = QPushButton('Generate')
        button.clicked.connect(self.show_plot)
        main_layout.addWidget(button)
        # states
        self.is_shown = False

        # Set the central widget of the Window
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_ball(self):
        # create ball then return ball name
        def add_callback(data):
            print(data)
            self.list_balls_data += [data]
            self.list_balls_widget.addItem(data['name'])
            self.ball_window.close()
            del self.ball_window

        def cancel_callback():
            self.ball_window.close()
            del self.ball_window

        self.ball_window = BallWindow(
            ball_data={
                'name': f"ball {len(self.list_balls_data) + 1}",
                'color': 'white',
                'start_x': 0.,
                'start_y': 0.,
                'learn_rate': 0.1,
                'tolerance': 0.0001,
                'max_iter': 10000,
                'momentum': 0.
            }, mode='add', delete_callback=cancel_callback, save_callback=add_callback)
        self.ball_window.show()

    def get_ball(self, ball):
        idx = ball.row()
        ball_data = self.list_balls_data[idx]

        def delete_cb():
            del self.list_balls_data[idx]
            self.ball_window.close()
            self.list_balls_widget.takeItem(idx)
            del self.ball_window

        def save_cb(new_data):
            self.list_balls_data[idx] = new_data
            self.list_balls_widget.currentItem().setText(new_data['name'])
            self.ball_window.close()
            del self.ball_window

        self.ball_window = BallWindow(ball_data, mode='edit', delete_callback=delete_cb, save_callback=save_cb)
        self.ball_window.show()
        print(ball_data)

    def show_plot(self):
        func_str = self.expr.text()
        print('expr', func_str)
        if func_str != '' and func_str is not None and not self.is_shown:
            MainWindow.show_glfw(func_str, set_show_state=self.toggle_is_shown, balls=self.list_balls_data)
            self.toggle_is_shown()

    def toggle_is_shown(self):
        self.is_shown = not self.is_shown

    @staticmethod
    def show_glfw(func_str, set_show_state, balls):
        func_str = func_str.strip().strip('\n')
        equation_parser = EquationParser(func_str=func_str)
        sgd_optimizer = SGDOptimizer(equation_parser=equation_parser)

        glfw.init()
        window = Window()
        surface = ParametricSurface(equation_parser=equation_parser, slope_func=sgd_optimizer.gradient)
        surface.setup()

        for ball in balls:
            surface.add_ball(
                Ball(x=ball['start_x'],
                     y=ball['start_y'],
                     z=equation_parser.evaluate(ball['start_x'], ball['start_y']),
                     optimizer=sgd_optimizer,
                     color=ball['color'],
                     learn_rate=ball['learn_rate'],
                     momentum=ball['momentum'],
                     radius=0.2),
            )

        window.add(surface)
        window.show()
        glfw.terminate()
        set_show_state()
        del equation_parser
        del sgd_optimizer


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
