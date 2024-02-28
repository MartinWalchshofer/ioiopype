#Copyright © 2024 Martin Walchshofer

from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode

class Frame(ONode):
    def __init__(self):
        super().__init__()
        self.add_o_stream(OStream(0,'frame')) #todo extend type, range, etc.

    def __del__(self):
        super().__del__()

    def send_frame(self, frame):
        self.write(0, frame)