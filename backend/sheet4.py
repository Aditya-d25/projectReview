# backend/sheet4.py
from backend.commonBackend import (
    update_review_attendance,
    get_group_members_for_review,
    save_review_marks,
    get_review_marks,
    save_review_responses,
    get_review_responses
)


def update_review4_attendance(group_id, attendance):
    """Update review4_attendance for members"""
    return update_review_attendance(4, group_id, attendance)


def get_group_members(group_id):
    """Fetch all members of a group with their details for Review 4"""
    return get_group_members_for_review(4, group_id)


def save_review4_marks(marks_list):
    """Save or update Review 4 marks for multiple students using UPSERT"""
    return save_review_marks(4, marks_list)


def get_review4_marks(group_id):
    """Fetch existing Review 4 marks for a group"""
    return get_review_marks(4, group_id)


def save_review4_responses(group_id, date, comments, responses):
    """Save or update Review 4 questionnaire responses using UPSERT"""
    return save_review_responses(4, group_id, date, comments, responses)


def get_review4_responses(group_id):
    """Fetch Review 4 questionnaire responses for a group"""
    return get_review_responses(4, group_id)