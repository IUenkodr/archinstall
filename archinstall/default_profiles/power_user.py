from archinstall.default_profiles.profile import Profile, ProfileType

class PowerUserProfile(Profile):
    def __init__(self) -> None:
        super().__init__(
            name='Power User',
            profile_type=ProfileType.Custom,
            packages=[
                'eza',
                'bat',
                'ripgrep',
                'fd',
                'bottom',
                'zoxide',
                'fzf',
                'neovim',
            ],
        )

    def preview_text(self) -> str:
        return "Modern Rust-based CLI tooling (eza, bat, rg, fd, btm, zoxide, fzf, nvim)"
