const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
  // Getting data from the form
  const data = new FormData(this)
  console.log(data)
  fetch(`${this.action}`, {
    method: 'POST',
    body: data
  })
    .then(response => alert("Rating saved"))
    .catch(error => alert("Error"))
});

button = document.querySelector('button[name=donate]')
button.addEventListener('click', e => {
  Swal.fire({
    title: 'Enter how much do you want to donate',
    input: 'text',
    showCancelButton: true,
    confirmButtonText: 'Donate',
    showLoaderOnConfirm: true,
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Thank you!',
        'We appreciate your support.',
        'success'
      )
    }
  })
})




