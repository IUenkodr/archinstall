import re
from pathlib import Path
from typing import Union

from archinstall.lib.models.packages import Repository, ThirdPartyRepository
from archinstall.lib.models.pacman import PacmanConfiguration
from archinstall.lib.pathnames import PACMAN_CONF

class PacmanConfig:
    def __init__(self, target: Path | None):
        self._config_remote_path: Path | None = None

        if target:
            self._config_remote_path = target / PACMAN_CONF.relative_to_root()

        self._repositories: list[Union[Repository, ThirdPartyRepository]] = []

    def enable(self, repo: Union[Repository, ThirdPartyRepository] | list[Union[Repository, ThirdPartyRepository]]) -> None:
        if not isinstance(repo, list):
            repo = [repo]

        self._repositories += repo

    def apply(self) -> None:
        if not self._repositories:
            return

        repos_to_enable = []
        third_party_repos = []

        for repo in self._repositories:
            if isinstance(repo, Repository):
                if repo == Repository.Testing:
                    repos_to_enable.extend(['core-testing', 'extra-testing', 'multilib-testing'])
                else:
                    repos_to_enable.append(repo.value)
            elif isinstance(repo, ThirdPartyRepository):
                third_party_repos.append(repo)

        content = PACMAN_CONF.read_text().splitlines(keepends=True)

        # Handle standard repos (uncommenting)
        for row, line in enumerate(content):
            match = re.match(r'^#\s*\[(.*)\]', line)
            if match and match.group(1) in repos_to_enable:
                content[row] = re.sub(r'^#\s*', '', line)
                if row + 1 < len(content) and content[row + 1].lstrip().startswith('#'):
                    content[row + 1] = re.sub(r'^#\s*', '', content[row + 1])

        # Handle 3rd party repos (appending)
        for tp in third_party_repos:
            # Check if repo already exists to avoid duplicates
            if f"[{tp.name}]" not in "".join(content):
                content.append(f"\n[{tp.name}]\nServer = {tp.server}\n")

        with PACMAN_CONF.open('w') as f:
            f.writelines(content)

    def persist(self) -> None:
        if self._config_remote_path:
            PACMAN_CONF.copy(self._config_remote_path, preserve_metadata=True)

    def configure(self, pacman_config: PacmanConfiguration) -> None:
        if not self._config_remote_path or not self._config_remote_path.exists():
            return

        content = self._config_remote_path.read_text().splitlines()
        result = []

        for line in content:
            if re.match(r'^#?\s*ParallelDownloads', line):
                result.append(f'ParallelDownloads = {pacman_config.parallel_downloads}')
            elif re.match(r'^#?\s*Color\s*$', line):
                result.append('Color' if pacman_config.color else '#Color')
            else:
                result.append(line)

        self._config_remote_path.write_text('\n'.join(result) + '\n')
