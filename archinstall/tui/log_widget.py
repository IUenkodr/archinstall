from textual.widgets import Static
from textual.app import App
from rich.text import Text
from archinstall.lib.log import logger

class LogWidget(Static):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logs = []
        self.max_logs = 100
        
        # Register this widget as a listener to the global logger
        logger.add_listener(self.on_log_received)

    def on_log_received(self, level: int, content: str):
        level_name = "INFO"
        if level == 10: level_name = "DEBUG"
        elif level == 40: level_name = "ERROR"
        elif level == 30: level_name = "WARN"
        
        log_entry = f"[{level_name}] {content}"
        self.logs.append(log_entry)
        
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        # Textual requires UI updates to happen on the main thread
        self.app.call_from_thread(self.update_display)

    def update_display(self):
        text = Text()
        for log in self.logs:
            text.append(log + "\n")
        
        self.update(text)

    def toggle_visibility(self):
        self.styles.display = "block" if self.styles.display == "none" else "none"
