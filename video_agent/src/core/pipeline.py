"""
Main Pipeline Orchestrator
Coordinates the complete video editing workflow.
"""
from pathlib import Path
from typing import List, Optional, Dict, Union
from loguru import logger

from config.settings import settings
from config.instagram_specs import get_spec
from src.core.video_input import VideoInput
from src.core.video_output import VideoOutput
from src.models.editing_plan import EditingPlan


class VideoPipeline:
    """Main video processing pipeline."""

    def __init__(self, input_path: Path):
        """
        Initialize pipeline.

        Args:
            input_path: Path to input video
        """
        self.input_path = Path(input_path)
        self.video_input = VideoInput.load(self.input_path)
        self.metadata = self.video_input.extract_metadata()

        # Ensure directories exist
        settings.ensure_directories()

        logger.info(f"Pipeline initialized for: {self.input_path.name}")
        logger.info(f"Video info: {self.metadata.width}x{self.metadata.height}, "
                   f"{self.metadata.duration:.1f}s, {self.metadata.fps:.1f}fps")

    def process(
        self,
        target_formats: List[str],
        editing_plan: Optional[EditingPlan] = None,
    ) -> Dict[str, Path]:
        """
        Process video for specified formats.

        Args:
            target_formats: List of Instagram format names
            editing_plan: Optional pre-computed editing plan

        Returns:
            Dictionary mapping format names to output paths
        """
        logger.info(f"Processing video for formats: {', '.join(target_formats)}")

        outputs = {}

        for format_name in target_formats:
            try:
                logger.info(f"Processing format: {format_name}")
                spec = get_spec(format_name)

                # TODO: Apply AI-driven editing
                # For now, just do basic export with format conversion
                output_path = VideoOutput.export_for_format(
                    self.input_path,
                    format_name,
                    settings.OUTPUT_DIR
                )

                # Validate output
                if VideoOutput.validate_output(output_path, spec):
                    outputs[format_name] = output_path
                    logger.success(f"✓ {format_name}: {output_path}")
                else:
                    logger.error(f"✗ {format_name}: Validation failed")
                    outputs[format_name] = None

            except Exception as e:
                logger.error(f"Failed to process {format_name}: {e}")
                outputs[format_name] = None

        return outputs

    def analyze(self) -> dict:
        """
        Analyze video content (Phase 2 - not yet implemented).

        Returns:
            Analysis results
        """
        logger.info("Analyzing video content...")

        # TODO: Implement analysis
        # - Extract frames
        # - Detect scenes
        # - Analyze audio
        # - Score content

        analysis = {
            'metadata': self.metadata.to_dict(),
            'scenes': [],
            'audio': {},
            'frames': [],
        }

        return analysis

    def create_editing_plan(
        self,
        format_name: str,
        analysis: Optional[dict] = None,
    ) -> EditingPlan:
        """
        Create editing plan using AI (Phase 3 - not yet implemented).

        Args:
            format_name: Target Instagram format
            analysis: Optional pre-computed analysis

        Returns:
            EditingPlan object
        """
        logger.info(f"Creating editing plan for {format_name}...")

        # TODO: Implement AI decision engine
        # - Analyze frames with Claude Vision
        # - Make crop decisions
        # - Select highlights
        # - Generate captions
        # - Choose effects

        plan = EditingPlan(format_name=format_name)

        return plan

    @staticmethod
    def process_video(
        input_path: Union[str, Path],
        target_formats: List[str],
    ) -> Dict[str, Path]:
        """
        Convenience method to process a video in one call.

        Args:
            input_path: Path to input video
            target_formats: List of Instagram format names

        Returns:
            Dictionary mapping format names to output paths
        """
        pipeline = VideoPipeline(input_path)
        return pipeline.process(target_formats)


def quick_convert(
    input_path: Union[str, Path],
    format_name: str = 'stories',
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Quick convert video to Instagram format without AI processing.

    Args:
        input_path: Path to input video
        format_name: Instagram format name (default: 'stories')
        output_dir: Optional output directory

    Returns:
        Path to output video
    """
    input_path = Path(input_path)
    logger.info(f"Quick converting {input_path.name} to {format_name}...")

    return VideoOutput.export_for_format(
        input_path,
        format_name,
        output_dir or settings.OUTPUT_DIR
    )
