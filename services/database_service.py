"""
Database Service for Project Aura.
Handles all database operations for projects and documents.
"""

import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service for managing Project Aura database operations.
    """

    def __init__(self, db_path: str = 'project_aura.db'):
        """
        Initialize database service.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self) -> bool:
        """
        Initialize database with required tables.
        
        Returns:
            True if initialization successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create Projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    project_type TEXT NOT NULL,
                    client_name TEXT,
                    scope TEXT,
                    start_date TEXT,
                    duration_weeks INTEGER,
                    team_size INTEGER,
                    delivery_model TEXT,
                    status TEXT DEFAULT 'Draft',
                    extracted_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create Documents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    file_type TEXT,
                    extracted_text TEXT,
                    file_size INTEGER,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            # Create Deliverables table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deliverables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    deliverable_name TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'Planned',
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            # Create Team Members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    count INTEGER DEFAULT 1,
                    resource_allocated BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            # Create Risks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS risks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    risk_description TEXT NOT NULL,
                    severity TEXT,
                    mitigation TEXT,
                    status TEXT DEFAULT 'Identified',
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Database initialized successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            return False

    def create_project(self, project_data: Dict[str, Any]) -> Optional[int]:
        """
        Create a new project.
        
        Args:
            project_data: Dictionary with project information
        
        Returns:
            Project ID if successful, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO projects (
                    project_name, project_type, client_name, scope,
                    start_date, duration_weeks, team_size, delivery_model,
                    extracted_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_data.get('project_name', 'Untitled Project'),
                project_data.get('project_type'),
                project_data.get('client_name'),
                project_data.get('scope'),
                project_data.get('start_date'),
                project_data.get('duration_weeks'),
                project_data.get('team_size'),
                project_data.get('delivery_model'),
                str(project_data.get('analysis', {}))
            ))
            
            project_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Project created with ID: {project_id}")
            return project_id
        
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            return None

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a project by ID.
        
        Args:
            project_id: Project ID
        
        Returns:
            Project dictionary or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        
        except Exception as e:
            logger.error(f"Error retrieving project: {str(e)}")
            return None

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieve all projects.
        
        Returns:
            List of project dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error retrieving projects: {str(e)}")
            return []

    def update_project(self, project_id: int, project_data: Dict[str, Any]) -> bool:
        """
        Update a project.
        
        Args:
            project_id: Project ID
            project_data: Dictionary with updated data
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            update_fields = []
            values = []
            
            for key, value in project_data.items():
                if key != 'id':
                    update_fields.append(f"{key} = ?")
                    values.append(value)
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(project_id)
            
            query = f"UPDATE projects SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Project {project_id} updated")
            return True
        
        except Exception as e:
            logger.error(f"Error updating project: {str(e)}")
            return False

    def add_document_to_project(self, project_id: int, doc_data: Dict[str, Any]) -> Optional[int]:
        """
        Add a document to a project.
        
        Args:
            project_id: Project ID
            doc_data: Document data
        
        Returns:
            Document ID if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO documents (
                    project_id, filename, file_type, extracted_text, file_size
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                project_id,
                doc_data.get('filename'),
                doc_data.get('extension'),
                doc_data.get('text'),
                doc_data.get('file_size', 0)
            ))
            
            doc_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return doc_id
        
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            return None

    def add_deliverables(self, project_id: int, deliverables: List[str]) -> bool:
        """
        Add deliverables to a project.
        
        Args:
            project_id: Project ID
            deliverables: List of deliverable names
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for deliverable in deliverables:
                cursor.execute('''
                    INSERT INTO deliverables (project_id, deliverable_name)
                    VALUES (?, ?)
                ''', (project_id, deliverable))
            
            conn.commit()
            conn.close()
            
            return True
        
        except Exception as e:
            logger.error(f"Error adding deliverables: {str(e)}")
            return False

    def add_team_members(self, project_id: int, team_breakdown: Dict[str, int]) -> bool:
        """
        Add team members to a project.
        
        Args:
            project_id: Project ID
            team_breakdown: Dictionary with roles and counts
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for role, count in team_breakdown.items():
                cursor.execute('''
                    INSERT INTO team_members (project_id, role, count)
                    VALUES (?, ?, ?)
                ''', (project_id, role, count))
            
            conn.commit()
            conn.close()
            
            return True
        
        except Exception as e:
            logger.error(f"Error adding team members: {str(e)}")
            return False

    def add_risks(self, project_id: int, risks: List[Dict[str, str]]) -> bool:
        """
        Add risks to a project.
        
        Args:
            project_id: Project ID
            risks: List of risk dictionaries
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for risk in risks:
                cursor.execute('''
                    INSERT INTO risks (project_id, risk_description, severity, mitigation)
                    VALUES (?, ?, ?, ?)
                ''', (
                    project_id,
                    risk.get('description'),
                    risk.get('severity'),
                    risk.get('mitigation')
                ))
            
            conn.commit()
            conn.close()
            
            return True
        
        except Exception as e:
            logger.error(f"Error adding risks: {str(e)}")
            return False

    def get_project_summary(self, project_id: int) -> Dict[str, Any]:
        """
        Get complete project summary.
        
        Args:
            project_id: Project ID
        
        Returns:
            Project summary dictionary
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get project
            cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            project = dict(cursor.fetchone())
            
            # Get documents
            cursor.execute('SELECT * FROM documents WHERE project_id = ?', (project_id,))
            documents = [dict(row) for row in cursor.fetchall()]
            
            # Get deliverables
            cursor.execute('SELECT * FROM deliverables WHERE project_id = ?', (project_id,))
            deliverables = [dict(row) for row in cursor.fetchall()]
            
            # Get team members
            cursor.execute('SELECT * FROM team_members WHERE project_id = ?', (project_id,))
            team_members = [dict(row) for row in cursor.fetchall()]
            
            # Get risks
            cursor.execute('SELECT * FROM risks WHERE project_id = ?', (project_id,))
            risks = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            return {
                'project': project,
                'documents': documents,
                'deliverables': deliverables,
                'team_members': team_members,
                'risks': risks
            }
        
        except Exception as e:
            logger.error(f"Error getting project summary: {str(e)}")
            return {}
