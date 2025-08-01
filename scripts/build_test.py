#!/usr/bin/env python3
"""Simple build test to validate PyPI publishing readiness."""

import subprocess
import sys
from pathlib import Path


def main():
    print("🧞 Automagik Hive - Build Test")
    print("=" * 40)

    # Clean and build
    print("🧹 Cleaning...")
    subprocess.run(["rm", "-rf", "dist"], check=True)

    print("🏗️ Building...")
    subprocess.run(["uv", "build"], check=True)

    # Check files exist
    wheel_files = list(Path("dist").glob("*.whl"))
    tar_files = list(Path("dist").glob("*.tar.gz"))

    print(
        f"✅ Built {len(wheel_files)} wheel(s) and {len(tar_files)} source distribution(s)"
    )

    # Check wheel contents
    if wheel_files:
        wheel_file = wheel_files[0]
        result = subprocess.run(
            ["uv", "run", "python", "-m", "zipfile", "-l", str(wheel_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        if "cli/" in result.stdout and "entry_points.txt" in result.stdout:
            print("✅ CLI module and entry points included")
        else:
            print("❌ CLI module or entry points missing")
            return False

        # Check entry points content
        subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-m",
                "zipfile",
                "-e",
                str(wheel_file),
                "/tmp/wheel_check",
            ],
            check=True,
        )

        entry_file = (
            Path("/tmp/wheel_check")
            / f"{wheel_file.stem}.dist-info"
            / "entry_points.txt"
        )
        if entry_file.exists():
            content = entry_file.read_text()
            print(f"📋 Entry points:\n{content}")
            if "automagik-hive = cli.main:main" in content:
                print("✅ Entry point correctly configured")
            else:
                print("❌ Entry point incorrect")
                return False

    print("\n🎉 Build test successful!")
    print("📦 Package is ready for PyPI publishing")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
