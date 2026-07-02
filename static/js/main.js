// main.js — students will add JavaScript here as features are built

document.querySelectorAll(".delete-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
        if (!confirm("Delete this expense? This can't be undone.")) {
            event.preventDefault();
        }
    });
});
