// Modal functionality
let deleteIndex = null;

function confirmDelete(index, name) {
  deleteIndex = index;
  document.getElementById('userName').textContent = name;
  document.getElementById('deleteModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('deleteModal').style.display = 'none';
}

function deleteUser() {
  document.getElementById('deleteForm').action = '/delete/' + deleteIndex;
  document.getElementById('deleteForm').submit();
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Delete buttons
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', function() {
      const index = this.dataset.index;
      const name = this.dataset.name;
      confirmDelete(index, name);
    });
  });

  // Modal buttons
  document.getElementById('noBtn').addEventListener('click', closeModal);
  document.getElementById('yesBtn').addEventListener('click', deleteUser);
});