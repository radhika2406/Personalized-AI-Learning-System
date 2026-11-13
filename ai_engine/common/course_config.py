"""
course_config.py

Configuration and registry for all 3 categories and 12 courses in the
Personalized AI Learning System.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any

# Root directory of courses data
COURSES_ROOT = Path("courses")

# The three main academic categories
CATEGORIES = {
    "programming": {
        "id": "programming",
        "name": "Programming",
        "description": "Core software development, object-oriented concepts, and algorithmic foundations.",
        "course_ids": ["python", "java", "cpp", "dsa"]
    },
    "ai_ml_data_science": {
        "id": "ai_ml_data_science",
        "name": "AI, ML and Data Science",
        "description": "Artificial intelligence, machine learning, deep neural architectures, and data analytics.",
        "course_ids": ["machine_learning", "deep_learning", "data_science", "neural_networks"]
    },
    "computer_science": {
        "id": "computer_science",
        "name": "Computer Science",
        "description": "Core systems topics including database systems, operating systems, networking, and OOP.",
        "course_ids": ["dbms", "operating_systems", "computer_networks", "oop"]
    }
}

# The 12 full courses
COURSES = {
    # Category A: Programming
    "python": {
        "id": "python",
        "name": "Python",
        "category": "programming",
        "category_name": "Programming",
        "path": COURSES_ROOT / "programming" / "python",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "java": {
        "id": "java",
        "name": "Java",
        "category": "programming",
        "category_name": "Programming",
        "path": COURSES_ROOT / "programming" / "java",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "cpp": {
        "id": "cpp",
        "name": "C++",
        "category": "programming",
        "category_name": "Programming",
        "path": COURSES_ROOT / "programming" / "cpp",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "dsa": {
        "id": "dsa",
        "name": "Data Structures and Algorithms (DSA)",
        "category": "programming",
        "category_name": "Programming",
        "path": COURSES_ROOT / "programming" / "dsa",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },

    # Category B: AI, ML and Data Science
    "machine_learning": {
        "id": "machine_learning",
        "name": "Machine Learning",
        "category": "ai_ml_data_science",
        "category_name": "AI, ML and Data Science",
        "path": COURSES_ROOT / "ai_ml_data_science" / "machine_learning",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "deep_learning": {
        "id": "deep_learning",
        "name": "Deep Learning",
        "category": "ai_ml_data_science",
        "category_name": "AI, ML and Data Science",
        "path": COURSES_ROOT / "ai_ml_data_science" / "deep_learning",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "data_science": {
        "id": "data_science",
        "name": "Data Science",
        "category": "ai_ml_data_science",
        "category_name": "AI, ML and Data Science",
        "path": COURSES_ROOT / "ai_ml_data_science" / "data_science",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "neural_networks": {
        "id": "neural_networks",
        "name": "Neural Networks",
        "category": "ai_ml_data_science",
        "category_name": "AI, ML and Data Science",
        "path": COURSES_ROOT / "ai_ml_data_science" / "neural_networks",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },

    # Category C: Computer Science
    "dbms": {
        "id": "dbms",
        "name": "DBMS",
        "category": "computer_science",
        "category_name": "Computer Science",
        "path": COURSES_ROOT / "computer_science" / "dbms",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "operating_systems": {
        "id": "operating_systems",
        "name": "Operating Systems",
        "category": "computer_science",
        "category_name": "Computer Science",
        "path": COURSES_ROOT / "computer_science" / "operating_systems",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "computer_networks": {
        "id": "computer_networks",
        "name": "Computer Networks",
        "category": "computer_science",
        "category_name": "Computer Science",
        "path": COURSES_ROOT / "computer_science" / "computer_networks",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    },
    "oop": {
        "id": "oop",
        "name": "Object-Oriented Programming (OOP)",
        "category": "computer_science",
        "category_name": "Computer Science",
        "path": COURSES_ROOT / "computer_science" / "oop",
        "default_checkpoints": {"stage_1_easy_exam": 10, "stage_2_medium_exam": 15, "stage_3_hard_exam": 16}
    }
}


def list_categories() -> List[str]:
    """Return all category identifiers."""
    return list(CATEGORIES.keys())


def get_category(category_id: str) -> Optional[Dict[str, Any]]:
    """Get category metadata by category identifier."""
    return CATEGORIES.get(category_id)


def list_courses() -> List[str]:
    """Return all 12 course identifiers."""
    return list(COURSES.keys())


def get_course(course_id: str) -> Optional[Dict[str, Any]]:
    """Get course metadata by course identifier."""
    return COURSES.get(course_id)


def get_courses_by_category(category_id: str) -> List[Dict[str, Any]]:
    """Return list of course dicts belonging to a category."""
    cat = CATEGORIES.get(category_id)
    if not cat:
        return []
    return [COURSES[cid] for cid in cat["course_ids"] if cid in COURSES]


def get_course_checkpoints(course_id: str) -> Dict[str, int]:
    """Return examination unlocking checkpoints for a course."""
    course = COURSES.get(course_id)
    if not course:
        raise ValueError(f"Unknown course_id: {course_id}")
    return course["default_checkpoints"]
