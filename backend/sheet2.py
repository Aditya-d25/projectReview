# backend/sheet2.py
from backend.commonBackend import (
    update_review_attendance,
    get_group_members_for_review,
    save_review_marks,
    get_review_marks,
    save_review_responses,
    get_review_responses
)


def update_review2_attendance(group_id, attendance):
    """Update review2_attendance for members"""
    return update_review_attendance(2, group_id, attendance)


def get_group_members(group_id):
    """Fetch all members of a group with their details for Review 2"""
    return get_group_members_for_review(2, group_id)


def save_review2_marks(marks_list):
    """Save or update Review 2 marks for multiple students using UPSERT"""
    return save_review_marks(2, marks_list)


def get_review2_marks(group_id):
    """Fetch existing Review 2 marks for a group"""
    return get_review_marks(2, group_id)


def save_review2_responses(group_id, date, comments, responses):
    """Save or update Review 2 questionnaire responses using UPSERT"""
    return save_review_responses(2, group_id, date, comments, responses)


def get_review2_responses(group_id):
    """Fetch Review 2 questionnaire responses for a group"""
    return get_review_responses(2, group_id)