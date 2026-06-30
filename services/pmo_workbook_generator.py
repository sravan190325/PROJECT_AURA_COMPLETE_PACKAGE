"""
PMO-Grade Workbook Generator for Project Aura.
Generates professional, executive-ready workbooks with consolidated sheets.
Final optimized version for consulting deliverables and executive stakeholders.
"""

import logging
from datetime import datetime
from typing import Dict, Any
from openpyxl import Workbook

from services.workbook_optimizer import PMOWorkbookOptimizer
from services.excel_formatter import ExcelFormatter

logger = logging.getLogger(__name__)


class PMOWorkbookGenerator:
    """
    Professional workbook generator producing PMO-grade deliverables.
    Creates a single, consolidated, executive-ready project management workbook.
    """

    def __init__(self, project_info: Dict, db_summary: Dict):
        """
        Initialize PMO workbook generator.

        Args:
            project_info: Project metadata (name, client, type, dates, team size, etc.)
            db_summary: Database project summary (risks, team, deliverables, dependencies)
        """
        self.project_info = project_info
        self.db_summary = db_summary
        self.workbook = None

    def generate(self, output_path: str) -> bool:
        """
        Generate complete PMO-grade workbook with 12 optimized sheets.

        Args:
            output_path: Path where workbook will be saved

        Returns:
            True if generation successful
        """
        try:
            logger.info(f"Generating PMO-grade workbook: {output_path}")

            self.workbook = Workbook()
            self.workbook.remove(self.workbook.active)

            # Generate 12 consolidated, optimized sheets in order
            logger.info("Creating Home page...")
            PMOWorkbookOptimizer.create_home_page(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Executive Dashboard...")
            PMOWorkbookOptimizer.create_executive_dashboard(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating AI Project Summary...")
            PMOWorkbookOptimizer.create_ai_project_summary(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Project Details...")
            PMOWorkbookOptimizer.create_project_details(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Project Roadmap...")
            PMOWorkbookOptimizer.create_project_roadmap(self.workbook, self.project_info)

            logger.info("Creating Detailed Project Plan...")
            PMOWorkbookOptimizer.create_detailed_project_plan(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Gantt Chart...")
            PMOWorkbookOptimizer.create_gantt_chart(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Milestone Tracker...")
            PMOWorkbookOptimizer.create_milestone_tracker(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Resource Plan...")
            PMOWorkbookOptimizer.create_resource_plan(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating RAID Register...")
            PMOWorkbookOptimizer.create_raid_register(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating RACI Matrix...")
            PMOWorkbookOptimizer.create_raci_matrix(self.workbook, self.project_info, self.db_summary)

            logger.info("Creating Weekly Status...")
            PMOWorkbookOptimizer.create_weekly_status(self.workbook, self.project_info)

            # Set workbook properties
            self._set_workbook_properties()

            # Save workbook
            self.workbook.save(output_path)
            logger.info(f"PMO workbook generated successfully: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error generating PMO workbook: {str(e)}", exc_info=True)
            return False

    def _set_workbook_properties(self):
        """Set professional workbook metadata."""
        client = self.project_info.get('client_name', 'Client')
        project = self.project_info.get('project_name', 'Project')
        project_type = self.project_info.get('project_type', 'Project')

        self.workbook.properties.title = f"{client} - {project} Management Workbook"
        self.workbook.properties.subject = f"{project_type} Project Planning"
        self.workbook.properties.creator = "Project Aura"
        self.workbook.properties.company = client
        self.workbook.properties.created = datetime.now()
        self.workbook.properties.modified = datetime.now()


class PMOWorkbookFactory:
    """Factory for creating workbook generators."""

    @staticmethod
    def create_pmo_generator(project_info: Dict, db_summary: Dict):
        """
        Create PMO-grade workbook generator.

        Args:
            project_info: Project information
            db_summary: Database summary

        Returns:
            PMOWorkbookGenerator instance
        """
        return PMOWorkbookGenerator(project_info, db_summary)
