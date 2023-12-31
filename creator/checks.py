import dataclasses
import subprocess
from packaging.version import parse as parse_version


@dataclasses.dataclass(kw_only=True)
class ProcessResult:
    returncode: int
    stdout: str
    stderr: str


def run_command(cmd):
    process = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True
    )
    return ProcessResult(
        returncode=process.returncode,
        stdout=process.stdout.decode("utf-8"),
        stderr=process.stderr.decode("utf-8"),
    )


class BinaryAvailableCheck:
    """Checks that a binary is available, and optionally checks the version of the binary. If the check goes through,
    additionnal context will be available to the caller containing ${NAME} and ${NAME}_VERSION for respectively the
    full path to this binary and its anounced version."""

    def __init__(self, binary, /, *, min_version=None, limit_version=None):
        self.name = binary
        self.context = {}
        self.min_version = parse_version(min_version) if min_version else None
        self.limit_version = parse_version(limit_version) if limit_version else None

    def check(self):
        upper_name = self.name.upper()
        if not upper_name in self.context:
            self.context[upper_name] = self._get_target()
        print(f"  {self.name} found at {self.context[upper_name]}")
        if not upper_name + "_VERSION" in self.context:
            self.context[upper_name + "_VERSION"] = self._get_version(
                self.context[upper_name]
            )

    def _get_version(self, target):
        """Parse the version as the binary gave it to us, compare to version constraints and retrun normalized version
        number."""
        version = self._get_raw_version(target)
        parsed_version = parse_version(version)
        if self.min_version and parsed_version < self.min_version:
            raise OSError(
                f"{self.name} version {version} is less than required version {self.min_version}"
            )
        if self.limit_version and parsed_version >= self.limit_version:
            raise OSError(
                f"{self.name} version {version} is greater or equal to the limit version {self.limit_version}"
            )
        return str(parsed_version)

    def _get_raw_version(self, target):
        """Get the version of the binary, by asking nicely."""
        try:
            version = run_command(f"{target} --version")
        except subprocess.CalledProcessError as exc:
            raise OSError(
                f'Could not get version of "{self.name}" ({target}).'
            ) from exc
        return version.stdout.strip()

    def _get_target(self):
        """Try to find the binary target, aka full path to binary."""
        try:
            exists = run_command(f"which {self.name}")
        except subprocess.CalledProcessError as exc:
            raise OSError(f'Binary for "{self.name}" not found.') from exc
        return exists.stdout.strip()


if __name__ == "__main__":
    c = BinaryAvailableCheck("pnpmxs", min_version="8", limit_version="9")
    c.check()
    print(c.context)
pnpm_is_available = BinaryAvailableCheck(
    "pnpm", min_version="8.13", limit_version="9.0"
)
npx_is_available = BinaryAvailableCheck("npx", min_version="9.8", limit_version="10.0")
prettier_is_available = BinaryAvailableCheck(
    "prettier", min_version="3.1", limit_version="3.2"
)
