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


