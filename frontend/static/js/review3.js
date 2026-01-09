// frontend/static/js/review3.js

const REVIEW_CONFIG = {
    reviewNumber: 3,
    criteria: [
        { name: "algo_study", label: "1. Detailed study of Algorithm(s) / Model / Hardware specification (As applicable)", max: 0, type: "text" },
        { name: "dataset_confirm", label: "2. Confirmation of Data set used (As applicable)", max: 0, type: "text" },
        { name: "implementation", label: "3. 50% Implementation (10M)", max: 10, type: "number" },
        { name: "partial_results", label: "4. Partial results obtained (7M)", max: 7, type: "number" },
        { name: "presentation_skills", label: "5. Presentation skills (4M)", max: 4, type: "number" },
        { name: "question_answer", label: "6. Question and Answer (4M)", max: 4, type: "number" },
        { name: "methodology_summary", label: "7. Summarize the methodologies/Algorithms implemented / to be implemented", max: 0, type: "text" }
    ],
    totalMarks: 25,
    previousReview: '/review2',
    nextReview: '/review4'
};

// DOM ready - Initialize with config
document.addEventListener("DOMContentLoaded", () => {
    initializeReviewPage(REVIEW_CONFIG);
});

// DOM ready - Initialize with config
document.addEventListener("DOMContentLoaded", () => {
    initializeReviewPage(REVIEW_CONFIG);
});