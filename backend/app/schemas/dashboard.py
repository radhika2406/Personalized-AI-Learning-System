from pydantic import BaseModel


class DashboardSummary(BaseModel):
    enrolled_courses: int
    learning_materials_completed: int
    quizzes_attempted: int
    average_quiz_percentage: float
    topics_tracked: int
    average_topic_mastery: float


class CourseDashboardSummary(BaseModel):
    course_id: int
    total_learning_materials: int
    completed_learning_materials: int
    learning_material_completion_percentage: float
    quizzes_attempted: int
    average_quiz_percentage: float
    topics_tracked: int
    average_topic_mastery: float


class TopicProgressSummary(BaseModel):
    topic_id: int
    topic_title: str
    sequence_number: int
    total_learning_materials: int
    completed_learning_materials: int
    completion_percentage: float
    quizzes_attempted: int
    mastery_score: float
