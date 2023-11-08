from typing import Any
from collections import deque

import imgui
import moderngl_window as mglw
from moderngl_window.context.base import KeyModifiers
from moderngl_window.integrations.imgui import ModernglWindowRenderer 

from settings import *
from camera import Camera


class WindowConfig(mglw.WindowConfig):
    gl_version = GL_VERSION
    title = TITLE
    window_size = RESOLUTION
    vsync = VSYNC
    resizable = RESIZEABLE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup imgui
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.ctx.enable(flags=mglw.moderngl.DEPTH_TEST | mglw.moderngl.CULL_FACE | mglw.moderngl.BLEND)

        self.wnd.mouse_exclusivity = True

        self.show_debug = False
        self.show_perf = True
        self.fps = []
        self.frametimes = deque(maxlen=15)

    def render(self, time: float, frametime: float):
        self.wnd.ctx.clear(0.2, 0.2, 0.2)
        self._calculate_fps(frametime, time)    

        if self.show_debug:
            self._debug_ui()
        
    def _calculate_fps(self, frametime: float, time: float):
        if not hasattr(self, 'prev_time'):
            self.prev_time = time
            self.frames = 0
            self.frametimes = []
        else:
            self.frames += 1
            self.frametimes.append(frametime)
            if time - self.prev_time >= 1.0:
                self.fps.append(self.frames / (time - self.prev_time))
                self.prev_time = time
                self.frames = 0
                self.frametimes = []

    def _debug_ui(self):
        imgui.new_frame()

        if imgui.begin("debug", self.show_debug):
            _, self.show_perf = imgui.checkbox("show perf", self.show_perf)
            imgui.end()

        if self.show_perf:
            imgui.set_next_window_size(0, 0)
            imgui.set_next_window_bg_alpha(0.0)
            opened, _ = imgui.begin("perf", closable=False, flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR)
            if opened:
                if self.fps:
                    imgui.text('fps')
                    imgui.same_line(spacing=52)
                    imgui.plot_lines(f"{self.fps[-1]:.0f}", np.array(self.fps, dtype="f"), graph_size=(150, 0))

                if self.frametimes:
                    imgui.text('frametime')
                    imgui.same_line(spacing=10)
                    imgui.plot_lines(f"{self.frametimes[-1]:.4f}", np.array(self.frametimes, dtype="f"), graph_size=(150, 0))

            imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def mouse_press_event(self, x: int, y: int, button: int):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)
    
    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def key_event(self, key: Any, action: Any, modifiers: KeyModifiers):
        self.imgui.key_event(key, action, modifiers)

        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.ESCAPE:
                self.wnd.close()
            
            if key == self.wnd.keys.F2:
                self.show_debug = not self.show_debug


if __name__ == "__main__":
    mglw.run_window_config(WindowConfig)