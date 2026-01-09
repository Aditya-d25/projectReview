# backend/sheet0.py
# This uses the common backend functions which work with the column-based approach

from backend.commonBackend import (
    update_review_attendance,
    get_group_members_for_review,
    save_review_marks,
    get_review_marks,
    save_review_responses,
    get_review_responses
)


def update_review0_attendance(group_id, attendance):
    """Update review0_attendance column in members table"""
    return update_review_attendance(0, group_id, attendance)


def get_group_members(group_id):
    """Fetch all members of a group with their details for Review 0"""
    return get_group_members_for_review(0, group_id)


def save_review0_marks(marks_list):
    """Save or update Review 0 marks for multiple students using UPSERT"""
    return save_review_marks(0, marks_list)


def get_review0_marks(group_id):
    """Fetch existing Review 0 marks for a group"""
    return get_review_marks(0, group_id)


def save_review0_responses(group_id, date, comments, responses):
    """Save or update Review 0 questionnaire responses using UPSERT"""
    return save_review_responses(0, group_id, date, comments, responses)


def get_review0_responses(group_id):
    """Fetch Review 0 questionnaire responses for a group"""
    return get_review_responses(0, group_id)