// ================= GLOBALS =================
let currentGroupId = null;
let summaryData = null;

// ================= MAIN LOAD FUNCTION =================
window.loadGroupData = async function () {
    const groupId = document.getElementById('group_id_select').value.trim();

    if (!groupId) {
        showStatus("Please enter a Group ID", "error");
        return;
    }

    currentGroupId = groupId;
    showStatus("Loading...", "loading");

    try {
        console.log("Fetching:", `/api/final-sheet/summary?group_id=${groupId}`);
        const res = await fetch(`/api/final-sheet/summary?group_id=${groupId}`);
        console.log("Response status:", res.status);

        if (!res.ok) throw new Error("Failed to load summary");

        summaryData = await res.json();

        // Show form and populate data
        document.getElementById('form-data').style.display = "block";
        document.getElementById('group_id').value = groupId;

        populateTable(summaryData);
        loadComments(groupId);

        showStatus("Data Loaded ✅", "success");
    } catch (err) {
        console.error(err);
        showStatus("Error loading data", "error");
    }
};

// ================= POPULATE TABLE =================
function populateTable(data) {
    const members = data.members || [];
    const reviewMarks = data.review_marks || {};

    const thead = document.getElementById('table-header');
    const tbody = document.getElementById('table-body');

    thead.innerHTML = `
        <tr>
            <th>Sr.No.</th>
            <th>Roll No.</th>
            <th>Name of the Student</th>
            <th>I</th>
            <th>II</th>
            <th>III</th>
            <th>IV</th>
            <th>Total</th>
            <th>Student Signature</th>
        </tr>
    `;

    tbody.innerHTML = "";

    members.forEach((member, idx) => {
        const r1 = member.review1_attendance ? (reviewMarks.review1?.[member.roll_no] || 0) : "Absent";
        const r2 = member.review2_attendance ? (reviewMarks.review2?.[member.roll_no] || 0) : "Absent";
        const r3 = member.review3_attendance ? (reviewMarks.review3?.[member.roll_no] || 0) : "Absent";
        const r4 = member.review4_attendance ? (reviewMarks.review4?.[member.roll_no] || 0) : "Absent";

        let total = 0;
        [r1, r2, r3, r4].forEach(r => { if (r !== "Absent") total += parseFloat(r); });

        const row = `
            <tr>
                <td>${idx + 1}</td>
                <td>${member.roll_no}</td>
                <td style="text-align:left">${member.student_name}</td>
                <td>${formatMark(r1)}</td>
                <td>${formatMark(r2)}</td>
                <td>${formatMark(r3)}</td>
                <td>${formatMark(r4)}</td>
                <td>${total.toFixed(1)}</td>
                <td></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function formatMark(val) {
    return val === "Absent" ? `<span class="absent-mark">${val}</span>` : parseFloat(val).toFixed(1);
}

// ================= COMMENTS LOADING =================
async function loadComments(groupId) {
    const res = await fetch(`/api/final-sheet/comments?group_id=${groupId}`);
    if (res.ok) {
        const data = await res.json();
        document.getElementById('comments').value = data.comments || '';
    }
}

// ================= STATUS MESSAGE =================
function showStatus(msg, type) {
    const div = document.getElementById('status-message');
    div.textContent = msg;
    div.style.color = type === "error" ? "red" : type === "success" ? "green" : "black";
}

// ================= BUTTON FUNCTIONS =================
window.previousReview = function () {
    window.location.href = "/review4";
};

window.submitForm = function () {
    alert("PDF generation not yet implemented!");
};
