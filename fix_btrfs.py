import sys

file_path = 'archinstall/lib/disk/filesystem.py'
with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'if part_mod.fs_type == FilesystemType.BTRFS and part_mod.is_create_or_modify():' in line:
        # We insert the optimization right after the if statement, before the call to create_btrfs_volumes
        # The original file has:
        # if part_mod.fs_type == FilesystemType.BTRFS and part_mod.is_create_or_modify():
        #     device_handler.create_btrfs_volumes(part_mod, enc_conf=self._enc_config)
        
        # To avoid duplicates, we check if we already added it (though we are running this once)
        # We only want to add the logic if the NEXT line is the device_handler call.
        pass 

# Actually, a simpler string replacement is safer if I'm precise.
