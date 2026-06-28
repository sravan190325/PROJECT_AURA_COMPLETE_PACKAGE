"""
Enhanced Workbook Generator for Project Aura.
Integrates new executive-grade sheets while preserving existing functionality.
Backwards compatible with current workbook generation.
"""

import logging
from datetime import datetime
from typing import Dict, Any
from openpyxl import Workbook

from services.workbook_generator import WorkbookGenerator
from services.workbook_enhancements import WorkbookEnhancements
from services.excel_formatter import ExcelFormatter

logger = logging.getLogger(__name__)


class EnhancedWorkbookGenerator(WorkbookGenerator):
    """
    Extended WorkbookGenerator with executive dashboard, roadmap, and advanced sheets.
    Preserves all existing functionality from parent class.
    """

    def __init__(self, project_info: Dict, db_summary: Dict, include_enhancements: bool = True):
        """
        Initialize enhanced workbook generator.

        Args:
            project_info: Project information dictionary
            db_summary: Database project summary
            include_enhancements: Include enhanced sheets (default: True for backward compatibility)
        """
        super().__init__(project_info, db_summary)
        self.include_enhancements = include_enhancements

    def generate(self, output_path: str) -> bool:
        """
        Generate complete enhanced workbook with executive sheets and professional formatting.

        Args:
            output_path: Path to save workbook

        Returns:
            True if successful
        """
        try:
            self.workbook = Workbook()
            self.workbook.remove(self.workbook.active)

            # Enhanced sheets (new functionality)
            if self.include_enhancements:
                logger.info("Adding enhanced enterprise sheets...")
                WorkbookEnhancements.create_executive_dashboard(self.workbook, self.project_info, self.db_summary)
                WorkbookEnhancements.create_project_roadmap(self.workbook, self.project_info)
                WorkbookEnhancements.create_enhanced_project_plan(self.workbook, self.project_info, self.db_summary)
                WorkbookEnhancements.create_milestone_tracker(self.workbook, self.project_info, self.db_summary)
                WorkbookEnhancements.create_resource_plan(self.workbook, self.project_info, self.db_summary)
                WorkbookEnhancements.create_raid_register(self.workbook, self.project_info, self.db_summary)
                WorkbookEnhancements.create_leave_capacity_planner(self.workbook, self.project_info, self.db_summary)
                WorkbookEnhancements.create_weekly_status_tracker(self.workbook, self.project_info)
                WorkbookEnhancements.create_ai_project_summary(self.workbook, self.project_info, self.db_summary)

            # Original sheets (preserved functionality)
            logger.info("Adding original project sheets...")
            self._create_project_details()
            self._create_project_charter()
            self._create_assumptions()
            self._create_staffing_plan()
            self._create_project_plan()
            self._create_wbs()
            self._create_risk_register()
            self._create_raci_matrix()
            self._create_leave_planner()
            self._create_project_tracker()

            # Add workbook properties for enterprise use
            self._set_workbook_properties()

            self.workbook.save(output_path)
            logger.info(f"Enhanced workbook generated successfully: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating enhanced workbook: {str(e)}")
            return False

    def _set_workbook_properties(self):
        """Set professional workbook properties."""
        self.workbook.properties.title = f"{self.client_name} - Project Plan"
        self.workbook.properties.subject = f"{self.project_type} Project Planning"
        self.workbook.properties.creator = "Project Aura"
        self.workbook.properties.created = datetime.now()
        self.workbook.properties.modified = datetime.now()

    def generate_without_enhancements(self, output_path: str) -> bool:
        """
        Generate original workbook without enhanced sheets (backward compatibility mode).

        Args:
            output_path: Path to save workbook

        Returns:
            True if successful
        """
        self.include_enhancements = False
        return self.generate(output_path)


class WorkbookGeneratorFactory:
    """Factory for creating workbook generators with appropriate configuration."""

    @staticmethod
    def create_generator(project_info: Dict, db_summary: Dict, enhanced: bool = True):
        """
        Create appropriate workbook generator instance.

        Args:
            project_info: Project information
            db_summary: Database summary
            enhanced: Use enhanced generator (True) or original (False)

        Returns:
            WorkbookGenerator or EnhancedWorkbookGenerator instance
        """
        if enhanced:
            return EnhancedWorkbookGenerator(project_info, db_summary, include_enhancements=True)
        else:
            return WorkbookGenerator(project_info, db_summary)

    @staticmethod
    def create_enhanced_generator(project_info: Dict, db_summary: Dict):
        """Create enhanced workbook generator."""
        return EnhancedWorkbookGenerator(project_info, db_summary, include_enhancements=True)

    @staticmethod
    def create_standard_generator(project_info: Dict, db_summary: Dict):
        """Create standard workbook generator (backward compatible)."""
        return WorkbookGenerator(project_info, db_summary)
