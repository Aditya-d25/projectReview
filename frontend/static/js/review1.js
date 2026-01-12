// frontend/static/js/review1.js

const REVIEW_CONFIG = {
    reviewNumber: 1,
    criteria: [
        { name: "understanding_topic", label: "1. Understanding background and Topic (2M)", max: 2 },
        { name: "project_scope", label: "2. Specifies Project Scope and Objective (2M)", max: 2 },
        { name: "literature_survey", label: "3. Literature Survey (5M)", max: 5 },
        { name: "project_planning", label: "4. Project Planning (4M)", max: 4 },
        { name: "contribution", label: "5. Contribution of the Student (4M)", max: 4 },
        { name: "presentation_skills", label: "6. Presentation Skills (4M)", max: 4 },
        { name: "question_answer", label: "7. Question and Answer (4M)", max: 4 }
    ],
    totalMarks: 25,
    previousReview: null, // No previous review
    nextReview: '/review2'
};

// DOM ready - Initialize with config
document.addEventListener("DOMContentLoaded", () => {
    initializeReviewPage(REVIEW_CONFIG);
});