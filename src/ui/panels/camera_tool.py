from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QToolButton,
    QToolTip,
    QVBoxLayout,
    QWidget,
)


class CameraControlsWidget(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.setWindowTitle("Camera Tool")
        self.engine = engine
        self._init_ui()
        self._setup_ui()

    def _init_ui(self):
        self.heading_widget = self._create_slider_with_reset(
            label="Heading",
            range=(0, 360),
            default_value=0,
            reset_function=self.reset_heading,
        )
        self.pitch_widget = self._create_slider_with_reset(
            label="Pitch",
            range=(0, 360),
            default_value=0,
            reset_function=self.reset_pitch,
        )
        self.roll_widget = self._create_slider_with_reset(
            label="Roll",
            range=(0, 360),
            default_value=0,
            reset_function=self.reset_roll,
        )

        self.fov_widget = self._create_slider_with_reset(
            label="FOV",
            range=(30, 120),
            default_value=50,
            reset_function=self.reset_fov,
        )

        self.x_position_widget = self._create_slider_with_reset(
            label="X Position",
            range=(-50, 50),
            default_value=0,
            reset_function=self.reset_x_position,
        )
        self.y_position_widget = self._create_slider_with_reset(
            label="Y Position",
            range=(-50, 50),
            default_value=-15,
            reset_function=self.reset_y_position,
        )
        self.z_position_widget = self._create_slider_with_reset(
            label="Z Position",
            range=(-25, 25),
            default_value=8,
            reset_function=self.reset_z_position,
        )

        self.rotation_speed_widget = self._create_slider_with_reset(
            label="Rotation Speed",
            range=(0, 100),
            default_value=0,
            reset_function=self.reset_rotation_speed,
        )

    def _setup_ui(self):
        # Create the main layout
        main_layout = QVBoxLayout()

        # Create the Orientation GroupBox
        orientation_group = QGroupBox("Orientation")
        orientation_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        orientation_layout = QFormLayout()
        orientation_layout.addRow("Heading: ", self.heading_widget)
        orientation_layout.addRow("Pitch: ", self.pitch_widget)
        orientation_layout.addRow("Roll: ", self.roll_widget)
        orientation_group.setLayout(orientation_layout)

        # Create the Position GroupBox
        position_group = QGroupBox("Position")
        position_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        position_layout = QFormLayout()
        position_layout.addRow("X: ", self.x_position_widget)
        position_layout.addRow("Y: ", self.y_position_widget)
        position_layout.addRow("Z: ", self.z_position_widget)
        position_group.setLayout(position_layout)

        # Create the Properties GroupBox
        properties_group = QGroupBox("Properties")
        properties_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        properties_layout = QFormLayout()
        properties_layout.addRow("FOV: ", self.fov_widget)
        properties_layout.addRow("Rotation Speed: ", self.rotation_speed_widget)
        properties_group.setLayout(properties_layout)

        main_layout.addWidget(orientation_group)
        main_layout.addWidget(position_group)
        main_layout.addWidget(properties_group)
        main_layout.addStretch()

        container_widget = QWidget()
        container_widget.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setMinimumWidth(200)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container_widget)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll_area)
        self.setLayout(outer_layout)

    def _create_slider_with_reset(self, label, range, default_value, reset_function):
        """Helper to create a slider with a reset button."""
        slider = QSlider(Qt.Horizontal)
        slider.setRange(*range)
        slider.setValue(default_value)
        reset_button = QToolButton(icon=QIcon.fromTheme("edit-undo"))
        reset_button.setToolTip(f"Reset {label} to default")
        reset_button.clicked.connect(reset_function)

        slider.valueChanged.connect(
            lambda value: self._update_engine_value(label, value)
        )

        slider.valueChanged.connect(
            lambda value: QToolTip.showText(QCursor.pos(), str(value))
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(slider)
        layout.addWidget(reset_button)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _update_engine_value(self, label, value):
        """Update the engine's value based on the slider's label."""
        if label == "Heading":
            self.engine.camera_controller.update_heading(value)
        elif label == "Pitch":
            self.engine.camera_controller.update_pitch(-value)
        elif label == "Roll":
            self.engine.camera_controller.update_roll(value)
        elif label == "FOV":
            self.engine.camera_controller.update_fov(value)
        elif label == "X Position":
            self.engine.camera_controller.update_position_x(value)
        elif label == "Y Position":
            self.engine.camera_controller.update_position_y(value)
        elif label == "Z Position":
            self.engine.camera_controller.update_position_z(value)
        elif label == "Rotation Speed":
            self._update_rotation_speed(value)

    def _update_rotation_speed(self, value):
        self.engine.camera_controller.update_rotation_speed(value)
        if value <= 0:
            self.engine.camera_controller.stop_rotation()
        else:
            self.engine.camera_controller.start_rotation()

    def reset_heading(self):
        self.engine.camera_controller.update_heading(0)
        self.heading_widget.findChild(QSlider).setValue(0)

    def reset_pitch(self):
        self.engine.camera_controller.update_pitch(0)
        self.pitch_widget.findChild(QSlider).setValue(0)

    def reset_roll(self):
        self.engine.camera_controller.update_roll(0)
        self.roll_widget.findChild(QSlider).setValue(0)

    def reset_fov(self):
        self.engine.camera_controller.update_fov(50)
        self.fov_widget.findChild(QSlider).setValue(50)

    def reset_x_position(self):
        self.engine.camera_controller.update_position_x(0)
        self.x_position_widget.findChild(QSlider).setValue(0)

    def reset_y_position(self):
        self.engine.camera_controller.update_position_y(-15)
        self.y_position_widget.findChild(QSlider).setValue(-15)

    def reset_z_position(self):
        self.engine.camera_controller.update_position_z(8)
        self.z_position_widget.findChild(QSlider).setValue(8)

    def reset_rotation_speed(self):
        self.engine.camera_controller.update_rotation_speed(0)
        self.rotation_speed_widget.findChild(QSlider).setValue(0)
