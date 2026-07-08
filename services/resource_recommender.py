"""
Resource recommendation service for matching project roles to a sample talent pool.
"""

import csv
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ResourceRecommender:
    """Match required roles to people based on role, skills, availability, and domain."""

    DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "talent_pool.csv"

    ROLE_SKILL_MAP = {
        "developer": ["react", "typescript", "javascript", "java", "python", "node", "api", "spring", "django", "frontend", "backend"],
        "frontend": ["react", "angular", "typescript", "javascript", "html", "css", "next"],
        "backend": ["java", "spring", "python", "django", "fastapi", "node", "api", "microservices"],
        "qa": ["qa", "testing", "selenium", "cypress", "playwright", "api testing", "regression", "appium"],
        "project manager": ["project manager", "pmo", "agile", "scrum", "stakeholder", "raid", "governance"],
        "pm": ["project manager", "pmo", "agile", "scrum", "stakeholder", "raid", "governance"],
        "tech lead": ["tech lead", "architecture", "code review", "microservices", "mentoring"],
        "architect": ["architect", "architecture", "cloud", "data modeling", "security", "migration"],
        "data engineer": ["data engineer", "python", "spark", "sql", "airflow", "databricks", "etl", "snowflake"],
        "data analyst": ["data analyst", "sql", "power bi", "tableau", "excel", "kpi"],
        "bi developer": ["bi developer", "power bi", "tableau", "dax", "dashboard", "reporting"],
        "devops": ["devops", "aws", "azure", "docker", "kubernetes", "terraform", "ci/cd"],
        "cloud": ["cloud", "aws", "azure", "gcp", "terraform", "kubernetes", "migration"],
        "security": ["security", "appsec", "oauth", "owasp", "pci", "iam", "soc2"],
        "ai": ["ai", "llm", "rag", "python", "langchain", "prompt", "vector"],
        "ui": ["ui", "ux", "figma", "design", "wireframes", "research"],
        "ux": ["ui", "ux", "figma", "design", "wireframes", "research"],
        "business analyst": ["business analyst", "requirements", "user stories", "uat", "process"],
        "scrum master": ["scrum master", "scrum", "kanban", "agile", "facilitation"],
        "mobile": ["mobile", "android", "ios", "react native", "flutter", "kotlin", "swift"],
    }

    ROLE_ALIASES = {
        "pm": "project manager",
        "qa engineer": "qa",
        "qa lead": "qa",
        "developers": "developer",
        "dev": "developer",
        "devops engineer": "devops",
        "ml ops": "ai",
        "ai engineer": "ai",
        "cloud engineer": "cloud",
        "cloud architect": "cloud",
        "ui/ux designer": "ui",
    }

    @classmethod
    def load_people(cls) -> List[Dict[str, str]]:
        if not cls.DATA_PATH.exists():
            return []

        with cls.DATA_PATH.open(newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    @classmethod
    def recommend_for_team(
        cls,
        team_requirements: Any,
        project_type: str = "",
        limit_per_role: int = 3,
    ) -> Dict[str, List[Dict[str, Any]]]:
        roles = cls._normalize_team_requirements(team_requirements)
        people = cls.load_people()

        recommendations: Dict[str, List[Dict[str, Any]]] = {}
        for role, count in roles.items():
            scored = [
                cls._score_person(role, person, project_type)
                for person in people
            ]
            ranked = [item for item in sorted(scored, key=lambda item: item[0], reverse=True) if item[0] > 0]

            recommendations[role] = [
                cls._format_candidate(person, score, reasons, count)
                for score, person, reasons in ranked[:limit_per_role]
            ]

        return recommendations

    @classmethod
    def _normalize_team_requirements(cls, team_requirements: Any) -> Dict[str, int]:
        if isinstance(team_requirements, dict):
            return {str(role): cls._safe_int(count) for role, count in team_requirements.items()}

        if isinstance(team_requirements, list):
            roles = {}
            for item in team_requirements:
                if isinstance(item, dict):
                    role = item.get("role") or item.get("name") or "Team Member"
                    roles[str(role)] = cls._safe_int(item.get("count") or item.get("quantity") or 1)
            return roles

        return {}

    @classmethod
    def _score_person(cls, role: str, person: Dict[str, str], project_type: str) -> Tuple[int, Dict[str, str], List[str]]:
        role_key = cls._canonical_role(role)
        role_text = f"{person.get('primary_role', '')} {person.get('skills', '')}".lower()
        project_text = project_type.lower()
        score = 0
        reasons: List[str] = []

        if role_key in person.get("primary_role", "").lower():
            score += 45
            reasons.append(f"primary role matches {role}")

        required_terms = cls.ROLE_SKILL_MAP.get(role_key, [role_key])
        matched_terms = [term for term in required_terms if term in role_text]
        if matched_terms:
            score += min(35, len(matched_terms) * 8)
            reasons.append("skills match: " + ", ".join(matched_terms[:4]))

        domain = person.get("domain", "").lower()
        if domain and any(token in project_text for token in domain.split()):
            score += 10
            reasons.append(f"domain fit: {person.get('domain')}")

        availability = person.get("availability", "").lower()
        if "available now" in availability:
            score += 12
            reasons.append("available now")
        elif "available soon" in availability:
            score += 8
            reasons.append(f"rolls off {person.get('project_end_date')}")

        try:
            if int(person.get("experience_years", 0)) >= 6:
                score += 5
        except ValueError:
            pass

        return score, person, reasons

    @classmethod
    def _format_candidate(
        cls,
        person: Dict[str, str],
        score: int,
        reasons: List[str],
        requested_count: int,
    ) -> Dict[str, Any]:
        return {
            "employee_id": person.get("employee_id"),
            "name": person.get("name"),
            "location": person.get("location"),
            "primary_role": person.get("primary_role"),
            "skills": person.get("skills"),
            "current_project": person.get("current_project"),
            "project_end_date": person.get("project_end_date"),
            "availability": person.get("availability"),
            "experience_years": cls._safe_int(person.get("experience_years")),
            "domain": person.get("domain"),
            "certifications": person.get("certifications"),
            "match_score": min(score, 100),
            "requested_count": requested_count,
            "why": "; ".join(reasons[:3]) if reasons else "closest role and skill match",
        }

    @classmethod
    def _canonical_role(cls, role: str) -> str:
        normalized = role.strip().lower()
        normalized = normalized.replace("/", " ").replace("-", " ")
        normalized = " ".join(normalized.split())

        if normalized in cls.ROLE_ALIASES:
            return cls.ROLE_ALIASES[normalized]

        for key in cls.ROLE_SKILL_MAP:
            if key in normalized:
                return key

        return normalized

    @staticmethod
    def _safe_int(value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 1
