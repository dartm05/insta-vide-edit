"""
Copy Editing Style Example
Demonstrates how to learn editing styles from reference videos and apply them to new content.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.analysis.style_analyzer import learn_from_video, apply_style_to_video
from src.models.editing_style import EditingStyle, get_preset_style, list_preset_styles
from config.settings import settings


def example_learn_from_video():
    """Example: Learn editing style from a reference video."""
    print("\n=== Learn Editing Style from Reference Video ===\n")

    reference_video = "reference_video.mp4"

    if not Path(reference_video).exists():
        print(f"Error: Reference video not found: {reference_video}")
        print("\nPlease provide a reference video that demonstrates the editing style you want to copy.")
        return

    try:
        # Analyze reference video
        print(f"Analyzing editing style from: {reference_video}")
        style = learn_from_video(
            reference_video,
            style_name="My Custom Style",
            save_to=Path("styles/my_custom_style.json")
        )

        # Display learned style
        print(f"\n✓ Style learned: {style.name}")
        print(f"\nStyle characteristics:")
        print(f"  Pace: {style.pace}")
        print(f"  Average shot duration: {style.average_shot_duration}s")
        print(f"  Crop style: {style.crop_style}")
        print(f"  Subject focus: {style.subject_focus}")
        print(f"  Captions: {'Yes' if style.has_captions else 'No'}")
        print(f"  Caption position: {style.caption_position}")
        print(f"  Color grade: {style.color_grade}")
        print(f"  Music presence: {style.music_presence}")

        print(f"\n✓ Style saved to: styles/my_custom_style.json")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_apply_learned_style():
    """Example: Apply a learned style to a new video."""
    print("\n=== Apply Learned Style to New Video ===\n")

    style_file = "styles/my_custom_style.json"
    input_video = "my_new_video.mp4"

    if not Path(style_file).exists():
        print(f"Error: Style file not found: {style_file}")
        print("\nRun example_learn_from_video() first to create a style.")
        return

    if not Path(input_video).exists():
        print(f"Error: Input video not found: {input_video}")
        return

    try:
        # Load the learned style
        print(f"Loading style from: {style_file}")
        style = EditingStyle.load(Path(style_file))
        print(f"✓ Loaded style: {style.name}")

        # Apply to new video
        print(f"\nApplying style to: {input_video}")
        output = apply_style_to_video(input_video, style, output_format='reels')

        print(f"\n✓ Success! Styled video created:")
        print(f"  Output: {output}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_use_preset_style():
    """Example: Use a built-in preset style."""
    print("\n=== Use Preset Editing Style ===\n")

    # Show available presets
    print("Available preset styles:")
    for i, style_name in enumerate(list_preset_styles(), 1):
        style = get_preset_style(style_name)
        print(f"  {i}. {style.name}")
        print(f"     {style.description}")
        print()

    input_video = "my_video.mp4"

    if not Path(input_video).exists():
        print(f"Note: Video file not found: {input_video}")
        return

    try:
        # Use a preset style
        style_name = "viral_tiktok"
        print(f"Using preset style: {style_name}")

        style = get_preset_style(style_name)
        print(f"\nStyle: {style.name}")
        print(f"Description: {style.description}")

        output = apply_style_to_video(input_video, style, output_format='reels')

        print(f"\n✓ Success! Video styled with {style.name}:")
        print(f"  Output: {output}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_compare_styles():
    """Example: Compare editing styles of two videos."""
    print("\n=== Compare Editing Styles ===\n")

    video1 = "video1.mp4"
    video2 = "video2.mp4"

    if not Path(video1).exists() or not Path(video2).exists():
        print("Error: Need two videos to compare")
        return

    try:
        from src.analysis.style_analyzer import StyleAnalyzer

        analyzer = StyleAnalyzer(Path(video1))
        differences = analyzer.compare_videos(Path(video2))

        print(f"Comparing {video1} and {video2}:\n")

        for category, values in differences.items():
            print(f"{category.replace('_', ' ').title()}:")
            print(f"  Video 1: {values['reference']}")
            print(f"  Video 2: {values['other']}")
            print()

    except Exception as e:
        print(f"\n✗ Error: {e}")


def example_workflow():
    """Example: Complete workflow - learn and apply style."""
    print("\n=== Complete Style Transfer Workflow ===\n")

    print("This workflow demonstrates:")
    print("1. Analyzing a viral video to learn its editing style")
    print("2. Saving the style for reuse")
    print("3. Applying that style to your own content")
    print()

    reference = "viral_reference.mp4"
    your_video = "your_content.mp4"
    style_name = "Viral Style"

    # Check files exist
    if not Path(reference).exists():
        print(f"Note: Reference video not found: {reference}")
        print("\nTo use this feature:")
        print("1. Find a video with editing you like (e.g., viral TikTok/Reel)")
        print("2. Run: learn_from_video('viral_video.mp4', 'Viral Style')")
        print("3. Apply to your videos: apply_style_to_video('your_video.mp4', style)")
        return

    if not Path(your_video).exists():
        print(f"Note: Your video not found: {your_video}")
        return

    try:
        # Step 1: Learn from viral video
        print("Step 1: Analyzing viral video...")
        style = learn_from_video(
            reference,
            style_name=style_name,
            save_to=Path(f"styles/{style_name.lower().replace(' ', '_')}.json")
        )
        print(f"✓ Learned style: {style.name}\n")

        # Step 2: Apply to your content
        print("Step 2: Applying style to your video...")
        output = apply_style_to_video(your_video, style, output_format='reels')
        print(f"✓ Output created: {output}\n")

        print("✓ Workflow complete!")
        print(f"\nYour video now has the same editing style as {reference}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Copy Editing Style - Learn and apply editing styles'
    )
    parser.add_argument(
        'command',
        nargs='?',
        choices=['learn', 'apply', 'presets', 'compare', 'workflow'],
        help='Command to run'
    )
    parser.add_argument(
        '--reference',
        help='Reference video to learn from'
    )
    parser.add_argument(
        '--input',
        help='Input video to apply style to'
    )
    parser.add_argument(
        '--style',
        help='Style file or preset name'
    )
    parser.add_argument(
        '--format',
        default='reels',
        choices=['stories', 'reels', 'feed_square', 'feed_portrait'],
        help='Output format'
    )

    args = parser.parse_args()

    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )

    if args.command == 'learn' and args.reference:
        # Learn from reference video
        style_name = Path(args.reference).stem.replace('_', ' ').title()
        style = learn_from_video(
            args.reference,
            style_name=style_name,
            save_to=Path(f"styles/{Path(args.reference).stem}.json")
        )
        print(f"\n✓ Style learned and saved: styles/{Path(args.reference).stem}.json")

    elif args.command == 'apply' and args.input and args.style:
        # Apply style to video
        if Path(args.style).exists():
            style = EditingStyle.load(Path(args.style))
        else:
            style = get_preset_style(args.style)

        output = apply_style_to_video(args.input, style, args.format)
        print(f"\n✓ Styled video created: {output}")

    elif args.command == 'presets':
        # Show presets
        example_use_preset_style()

    elif args.command == 'compare' and args.reference and args.input:
        # Compare videos
        from src.analysis.style_analyzer import StyleAnalyzer
        analyzer = StyleAnalyzer(Path(args.reference))
        differences = analyzer.compare_videos(Path(args.input))
        print("\nComparison:")
        for key, vals in differences.items():
            print(f"{key}: {vals}")

    else:
        # Run examples
        print("=" * 70)
        print("Copy Editing Style - Learn from Reference Videos")
        print("=" * 70)

        example_learn_from_video()
        example_use_preset_style()
        example_compare_styles()
        example_workflow()

        print("\n" + "=" * 70)
        print("Command-line usage:")
        print("  Learn:   python copy_editing_style.py learn --reference viral.mp4")
        print("  Apply:   python copy_editing_style.py apply --input my.mp4 --style viral")
        print("  Presets: python copy_editing_style.py presets")
        print("=" * 70)


if __name__ == '__main__':
    main()
