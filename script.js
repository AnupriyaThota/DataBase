document.addEventListener('DOMContentLoaded', () => {
    const dueDateSelect = document.getElementById('due_date');
    const paymentForm = document.getElementById('paymentForm');
    const recordsTableBody = document.querySelector('#recordsTable tbody');

    // Populate due date dynamically
    const dueDates = ['04/15', '06/15', '09/15', '01/15'];
    const currentYear = new Date().getFullYear();

    dueDates.forEach(date => {
        const option = document.createElement('option');
        const year = date === '01/15' ? currentYear + 1 : currentYear;
        option.value = `${year}-${date.replace('/', '-')}`;
        option.textContent = `${date}/${year}`;
        dueDateSelect.appendChild(option);
    });

    // Fetch and display records
    async function fetchRecords() {
        const response = await fetch('/view_records');
        const records = await response.json();
        displayRecords(records);
    }

    function displayRecords(records) {
        recordsTableBody.innerHTML = '';
        records.forEach(record => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${record.id}</td>
                <td>${record.company}</td>
                <td>${record.amount.toFixed(2)}</td>
                <td>${record.payment_date}</td>
                <td>${record.status}</td>
                <td>${record.due_date}</td>
                <td>
                    <button onclick="editRecord(${record.id})">Edit</button>
                    <button onclick="deleteRecord(${record.id})">Delete</button>
                </td>
            `;
            recordsTableBody.appendChild(row);
        });
    }

    // Form submission handler
    paymentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(paymentForm);
        const data = Object.fromEntries(formData.entries());

        await fetch('/add_record', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        paymentForm.reset();
        fetchRecords();
    });

    // Delete record function
    async function deleteRecord(id) {
        await fetch(`/delete_record/${id}`, { method: 'DELETE' });
        fetchRecords();
    }

    // Initialize page
    fetchRecords();
});
