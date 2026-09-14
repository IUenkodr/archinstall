import sys

file_path = 'archinstall/lib/pacman/config.py'
with open(file_path, 'r') as f:
    lines = f.readlines()

# We need to update the apply method to handle ThirdPartyRepository
# and add an enable_third_party method.

# Find the apply method and modify it.
# The original apply method only handles the standard Repository Enum.

new_lines = []
in_apply = False
found_apply_end = False

for line in lines:
    if 'def apply(self) -> None:' in line:
        in_apply = True
    
    new_lines.append(line)
    
    # When we hit the end of the apply method (the next def or class)
    if in_apply and (line.startswith('    def ') or line.startswith('class ') or line.strip() == ''):
        # This is a bit risky with line-by-line. Let's do a full content replacement.
        pass

# I'll use a full replacement for the PacmanConfig class to be safe.
