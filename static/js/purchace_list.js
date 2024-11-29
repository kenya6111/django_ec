document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.history-row');
    rows.forEach(row => {
        row.addEventListener('click', function() {
            window.location = this.dataset.href;  // data-href 属性の値に遷移
        });
    });
});