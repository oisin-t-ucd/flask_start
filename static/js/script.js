// Modal functionality
let deleteIndex = null;

function confirmDelete(index, task) {
  deleteIndex = index;
  document.getElementById('taskName').textContent = task;
  document.getElementById('deleteModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('deleteModal').style.display = 'none';
}

function deleteTodo() {
  document.getElementById('deleteForm').action = '/delete/' + deleteIndex;
  document.getElementById('deleteForm').submit();
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Delete buttons
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', function() {
      const index = this.dataset.index;
      const task = this.dataset.task;
      confirmDelete(index, task);
    });
  });

  // Modal buttons
  document.getElementById('noBtn').addEventListener('click', closeModal);
  document.getElementById('yesBtn').addEventListener('click', deleteTodo);
});
