# backend/sheet3.py
from backend.commonBackend import (
    update_review_attendance,
    get_group_members_for_review,
    save_review_marks,
    get_review_marks,
    save_review_responses,
    get_review_responses
)


def update_review3_attendance(group_id, attendance):
    """Update review3_attendance for members"""
    return update_review_attendance(3, group_id, attendance)


def get_group_members(group_id):
    """Fetch all members of a group with their details for Review 3"""
    return get_group_members_for_review(3, group_id)


def save_review3_marks(marks_list):
    """Save or update Review 3 marks for multiple students using UPSERT"""
    return save_review_marks(3, marks_list)


def get_review3_marks(group_id):
    """Fetch existing Review 3 marks for a group"""
    return get_review_marks(3, group_id)


def save_review3_responses(group_id, date, comments, responses):
    """Save or update Review 3 questionnaire responses using UPSERT"""
    return save_review_responses(3, group_id, date, comments, responses)


def get_review3_responses(group_id):
    """Fetch Review 3 questionnaire responses for a group"""
    return get_review_responses(3, group_id)