"""
Basic Video Editing Example
Demonstrates simple usage of the video editing platform.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.core.pipeline import VideoPipeline, quick_convert
from config.settings import settings


def example_quick_convert():
    """Example: Quick convert to Instagram Stories format."""
    print("\n=== Quick Convert Example ===\n")

    # Replace with your video path
    input_video = "sample_video.mp4"

    if not Path(input_video).exists():
        print(f"Error: Video file not found: {input_video}")
        print("Please provide a valid video file path.")
        return

    try:
        output_path = quick_convert(input_video, format_name='stories')
        print(f"\n✓ Success! Video converted to Instagram Stories format:")
        print(f"  Output: {output_path}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_multi_format():
    """Example: Convert to multiple Instagram formats."""
    print("\n=== Multi-Format Export Example ===\n")

    # Replace with your video path
    input_video = "sample_video.mp4"

    if not Path(input_video).exists():
        print(f"Error: Video file not found: {input_video}")
        print("Please provide a valid video file path.")
        return

    # Target formats
    formats = ['stories', 'reels', 'feed_square']

    try:
        # Create pipeline
        pipeline = VideoPipeline(input_video)

        # Show video info
        print(f"Input video: {pipeline.metadata.width}x{pipeline.metadata.height}, "
              f"{pipeline.metadata.duration:.1f}s")

        # Process for multiple formats
        print(f"\nProcessing for {len(formats)} formats...")
        outputs = pipeline.process(formats)

        # Display results
        print("\nResults:")
        for format_name, output_path in outputs.items():
            if output_path:
                print(f"  ✓ {format_name}: {output_path}")
            else:
                print(f"  ✗ {format_name}: Failed")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_with_validation():
    """Example: Check video compatibility before processing."""
    print("\n=== Validation Example ===\n")

    input_video = "sample_video.mp4"

    if not Path(input_video).exists():
        print(f"Error: Video file not found: {input_video}")
        return

    try:
        # Load video
        from src.core.video_input import VideoInput
        video = VideoInput.load(input_video)
        metadata = video.extract_metadata()

        print(f"Video: {metadata.file_path.name}")
        print(f"  Resolution: {metadata.width}x{metadata.height}")
        print(f"  Duration: {metadata.duration:.1f}s")
        print(f"  Aspect Ratio: {metadata.get_aspect_ratio_string()}")
        print(f"  FPS: {metadata.fps:.1f}")
        print(f"  Has Audio: {metadata.has_audio}")

        # Check compatibility with different formats
        print("\nFormat Compatibility:")
        for format_name in ['stories', 'reels', 'feed_square', 'feed_portrait']:
            is_valid, message = video.validate_for_format(format_name)
            status = "✓" if is_valid else "⚠"
            print(f"  {status} {format_name}: {message if not is_valid else 'Compatible'}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Instagram Video Editor - Basic Examples'
    )
    parser.add_argument(
        'video',
        nargs='?',
        help='Path to input video file'
    )
    parser.add_argument(
        '--formats',
        nargs='+',
        default=['stories'],
        help='Target formats (stories, reels, feed_square, feed_portrait)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory'
    )

    args = parser.parse_args()

    # Set output directory if specified
    if args.output_dir:
        settings.OUTPUT_DIR = args.output_dir

    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )

    if args.video:
        # Process specified video
        try:
            pipeline = VideoPipeline(args.video)
            outputs = pipeline.process(args.formats)

            print("\n=== Results ===")
            for format_name, output_path in outputs.items():
                if output_path:
                    print(f"✓ {format_name}: {output_path}")
                else:
                    print(f"✗ {format_name}: Failed")

        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)
    else:
        # Run examples
        print("=" * 60)
        print("Instagram Video Editor - Basic Examples")
        print("=" * 60)

        example_quick_convert()
        example_multi_format()
        example_with_validation()

        print("\n" + "=" * 60)
        print("To process your own video:")
        print("  python examples/basic_edit.py your_video.mp4 --formats stories reels")
        print("=" * 60)


if __name__ == '__main__':
    main()
