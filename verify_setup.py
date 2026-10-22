#!/usr/bin/env python3
"""
Setup Verification Script
Checks that all dependencies and requirements are properly installed.
"""
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_python_version():
    """Check Python version."""
    print("\n1. Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("   ❌ Python 3.9+ required")
        return False

    print("   ✓ Python version OK")
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\n2. Checking FFmpeg...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            check=True
        )
        version_line = result.stdout.split('\n')[0]
        print(f"   {version_line}")
        print("   ✓ FFmpeg installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ❌ FFmpeg not found")
        print("\n   Install FFmpeg:")
        print("     macOS:        brew install ffmpeg")
        print("     Ubuntu/Debian: sudo apt install ffmpeg")
        print("     Windows:      Download from https://ffmpeg.org/download.html")
        return False


def check_python_packages():
    """Check if required Python packages are installed."""
    print("\n3. Checking Python packages...")

    required_packages = [
        ('anthropic', 'anthropic'),
        ('pydantic', 'pydantic'),
        ('dotenv', 'python-dotenv'),
        ('loguru', 'loguru'),
        ('ffmpeg', 'ffmpeg-python'),
        ('cv2', 'opencv-python'),
        ('PIL', 'pillow'),
        ('pydub', 'pydub'),
        ('numpy', 'numpy'),
    ]

    all_ok = True
    installed = []
    missing = []

    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            installed.append(package_name)
            print(f"   ✓ {package_name}")
        except ImportError:
            missing.append(package_name)
            print(f"   ❌ {package_name} not installed")
            all_ok = False

    if not all_ok:
        print("\n   Install missing packages:")
        print("     pip install -r requirements.txt")

    return all_ok


def check_project_structure():
    """Check if project structure is correct."""
    print("\n4. Checking project structure...")

    required_dirs = [
        'config',
        'src',
        'src/core',
        'src/models',
        'src/utils',
        'src/analysis',
        'examples',
    ]

    required_files = [
        'requirements.txt',
        'README.md',
        '.env.example',
        'config/instagram_specs.py',
        'src/core/pipeline.py',
        'examples/basic_edit.py',
        'examples/copy_editing_style.py',
    ]

    all_ok = True

    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"   ✓ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ not found")
            all_ok = False

    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists() and file_path.is_file():
            print(f"   ✓ {file_name}")
        else:
            print(f"   ❌ {file_name} not found")
            all_ok = False

    return all_ok


def check_env_file():
    """Check if .env file exists and has API key."""
    print("\n5. Checking configuration...")

    env_file = Path('.env')
    if not env_file.exists():
        print("   ⚠ .env file not found")
        print("\n   Create .env file:")
        print("     cp .env.example .env")
        print("     # Edit .env and add your ANTHROPIC_API_KEY")
        return False

    print("   ✓ .env file exists")

    # Check if API key is set
    content = env_file.read_text()
    if 'ANTHROPIC_API_KEY=' in content:
        if 'your_api_key_here' in content or 'ANTHROPIC_API_KEY=\n' in content:
            print("   ⚠ ANTHROPIC_API_KEY not configured")
            print("     Edit .env and add your actual API key")
            return False
        else:
            print("   ✓ ANTHROPIC_API_KEY configured")
            return True
    else:
        print("   ⚠ ANTHROPIC_API_KEY not found in .env")
        return False


def test_basic_imports():
    """Test if core modules can be imported."""
    print("\n6. Testing core module imports...")

    modules_to_test = [
        'config.instagram_specs',
        'config.settings',
        'src.core.pipeline',
        'src.core.video_input',
        'src.core.video_output',
        'src.models.editing_style',
        'src.analysis.style_analyzer',
        'src.utils.ffmpeg_wrapper',
    ]

    all_ok = True

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✓ {module_name}")
        except Exception as e:
            print(f"   ❌ {module_name}: {e}")
            all_ok = False

    return all_ok


def main():
    """Main verification function."""
    print_header("Video Agent Setup Verification")

    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Python Packages", check_python_packages),
        ("Project Structure", check_project_structure),
        ("Configuration", check_env_file),
        ("Module Imports", test_basic_imports),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n   ❌ Error checking {name}: {e}")
            results.append((name, False))

    # Summary
    print_header("Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nPassed: {passed}/{total} checks\n")

    for name, result in results:
        status = "✓" if result else "❌"
        print(f"  {status} {name}")

    if passed == total:
        print("\n" + "=" * 60)
        print("  🎉 All checks passed! Your setup is ready.")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Try the examples:")
        print("     python examples/basic_edit.py")
        print("     python examples/copy_editing_style.py")
        print("\n  2. Read the documentation:")
        print("     - README.md for basic usage")
        print("     - STYLE_TRANSFER_GUIDE.md for style copying")
        print("     - FAQ.md for common questions")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("  ⚠ Some checks failed. Please fix the issues above.")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
