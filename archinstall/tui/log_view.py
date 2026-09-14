from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.live import Live
from typing import List

class LogView:
    def __init__(self, max_lines: int = 15):
        self.max_lines = max_lines
        self.buffer: List[str] = []
        self.visible = False

    def on_log(self, level: int, content: str):
        # format the log line: [LEVEL] Content
        level_name = "INFO"
        if level == 10: level_name = "DEBUG"
        elif level == 40: level_name = "ERROR"
        elif level == 30: level_name = "WARN"

        formatted_line = f"[{level_name}] {content}"
        self.buffer.append(formatted_line)
        
        # Keep buffer within max_lines
        if len(self.buffer) > self.max_lines:
            self.buffer.pop(0)

    def render(self):
        if not self.visible:
            return None
            
        log_text = Text()
        for line in self.buffer:
            log_text.append(line + "\n")
            
        return Panel(
            log_text, 
            title="[bold cyan]Live Install Log[/bold cyan]", 
            border_style="blue",
            expand=True
        )
