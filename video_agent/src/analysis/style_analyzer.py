"""
Style Analyzer
Analyzes reference videos to learn and replicate editing styles.
"""
from pathlib import Path
from typing import Optional, Union
from loguru import logger

from src.models.editing_style import EditingStyle
from src.core.video_input import VideoInput


class StyleAnalyzer:
    """
    Analyzes reference videos to extract editing style patterns.
    """

    def __init__(self, reference_video: Path):
        """
        Initialize style analyzer.

        Args:
            reference_video: Path to reference video
        """
        self.reference_video = Path(reference_video)
        self.video_input = VideoInput.load(self.reference_video)
        self.metadata = self.video_input.extract_metadata()

    def analyze_style(self, style_name: Optional[str] = None) -> EditingStyle:
        """
        Analyze reference video and extract editing style.

        Args:
            style_name: Optional name for the style

        Returns:
            EditingStyle object with learned patterns
        """
        logger.info(f"Analyzing editing style from: {self.reference_video.name}")

        if style_name is None:
            style_name = f"Style from {self.reference_video.stem}"

        # TODO: Implement full AI-powered style analysis
        # For now, create a basic style from video properties
        style = EditingStyle(
            name=style_name,
            description=f"Editing style learned from {self.reference_video.name}",
            source_video=self.reference_video,
            created_from='reference_video_analysis'
        )

        # Analyze basic properties
        style = self._analyze_basic_properties(style)

        logger.info(f"Style analysis complete: {style.name}")
        return style

    def _analyze_basic_properties(self, style: EditingStyle) -> EditingStyle:
        """
        Analyze basic video properties to infer style.

        Args:
            style: EditingStyle object to populate

        Returns:
            Updated EditingStyle object
        """
        # Infer pace from video duration and aspect ratio
        if self.metadata.duration < 30:
            style.pace = 'fast'
            style.average_shot_duration = 1.5
            style.min_shot_duration = 0.5
            style.max_shot_duration = 3.0
        elif self.metadata.duration < 60:
            style.pace = 'medium'
            style.average_shot_duration = 3.0
            style.min_shot_duration = 1.5
            style.max_shot_duration = 5.0
        else:
            style.pace = 'slow'
            style.average_shot_duration = 4.5
            style.min_shot_duration = 2.0
            style.max_shot_duration = 8.0

        # Infer crop style from aspect ratio
        aspect_str = self.metadata.get_aspect_ratio_string()
        if aspect_str == '9:16':
            style.crop_style = 'centered'
            style.subject_focus = 'face'
        elif aspect_str == '1:1':
            style.crop_style = 'centered'
            style.subject_focus = 'full_body'
        else:
            style.crop_style = 'rule_of_thirds'
            style.subject_focus = 'scene'

        # Patterns dictionary for future AI analysis
        style.patterns['reference_metadata'] = self.metadata.to_dict()

        return style

    def compare_videos(
        self,
        other_video: Path,
    ) -> dict:
        """
        Compare this video with another to identify style differences.

        Args:
            other_video: Path to video to compare

        Returns:
            Dictionary of differences
        """
        logger.info(f"Comparing {self.reference_video.name} with {other_video.name}")

        other_input = VideoInput.load(other_video)
        other_metadata = other_input.extract_metadata()

        differences = {
            'aspect_ratio': {
                'reference': self.metadata.get_aspect_ratio_string(),
                'other': other_metadata.get_aspect_ratio_string(),
            },
            'duration': {
                'reference': self.metadata.duration,
                'other': other_metadata.duration,
            },
            'resolution': {
                'reference': (self.metadata.width, self.metadata.height),
                'other': (other_metadata.width, other_metadata.height),
            },
            'fps': {
                'reference': self.metadata.fps,
                'other': other_metadata.fps,
            },
        }

        return differences

    @staticmethod
    def analyze_with_ai(reference_video: Path, style_name: Optional[str] = None) -> EditingStyle:
        """
        Use AI to deeply analyze editing style from reference video.
        This is a placeholder for Phase 3 AI integration.

        Args:
            reference_video: Path to reference video
            style_name: Optional style name

        Returns:
            EditingStyle with AI-extracted patterns
        """
        logger.warning("AI-powered style analysis not yet implemented. Using basic analysis.")

        analyzer = StyleAnalyzer(reference_video)
        return analyzer.analyze_style(style_name)


def learn_from_video(
    reference_video: Union[str, Path],
    style_name: Optional[str] = None,
    save_to: Optional[Path] = None,
) -> EditingStyle:
    """
    Learn editing style from a reference video.

    Args:
        reference_video: Path to reference video
        style_name: Optional name for the style
        save_to: Optional path to save the style JSON

    Returns:
        EditingStyle object

    Example:
        style = learn_from_video('viral_video.mp4', 'My Viral Style')
        style.save('styles/my_viral_style.json')
    """
    analyzer = StyleAnalyzer(Path(reference_video))
    style = analyzer.analyze_style(style_name)

    if save_to:
        style.save(save_to)

    return style


def apply_style_to_video(
    input_video: Union[str, Path],
    style: EditingStyle,
    output_format: str = 'stories',
) -> Path:
    """
    Apply a learned editing style to a new video.

    Args:
        input_video: Path to input video
        style: EditingStyle to apply
        output_format: Target Instagram format

    Returns:
        Path to processed video

    Example:
        style = EditingStyle.load('styles/viral_style.json')
        output = apply_style_to_video('my_video.mp4', style, 'reels')
    """
    logger.info(f"Applying style '{style.name}' to {Path(input_video).name}")

    # TODO: Implement style application in pipeline
    # This will be integrated with the AI decision engine in Phase 3

    from src.core.pipeline import VideoPipeline

    pipeline = VideoPipeline(input_video)

    # For now, just do basic processing
    # In Phase 3, the style will guide AI decisions
    outputs = pipeline.process([output_format])

    logger.info(f"Style applied. Output: {outputs[output_format]}")
    return outputs[output_format]
