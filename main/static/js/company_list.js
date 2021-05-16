deleteButton = document.getElementById('b_delete')
const deleteForm = document.querySelector('form[name=erase]');
console.log(deleteForm)
deleteForm.addEventListener("submit", e => {
  e.preventDefault()
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!'
  }).then((result) => {
    if (result.isConfirmed) {
      const data = new FormData(deleteForm)
      fetch(`${deleteForm.action}`, {
        method: 'POST',
        body: data
      }).then(r => console.log("success"))
        .catch(e => console.log("error"))
      Swal.fire(
        'Deleted!',
        'Your company has been deleted.',
        'success'
      )
      document.location.reload()
    }
  })
})
