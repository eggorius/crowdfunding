let forms = document.querySelectorAll('.needs-validation')

forms.forEach(form => {
  form.addEventListener('keypress', event => {
    form.classList.add('was-validated')
  }, false)
})
$('#id_password, #id_confirm_password').on('keyup', function () {
  if ($('#id_password').val() === $('#id_confirm_password').val()) {
    $('#message').html('Matching').css('color', 'green');
  } else
    $('#message').html('Not Matching').css('color', 'red');
});