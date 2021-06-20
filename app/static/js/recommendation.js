$(document).ready(function() {
  $("#rec_form").on('submit', function(event) {
      event.preventDefault();
      $.get('get_recommendation?' + $('#rec_form').serialize(), function(content) {
          if (content == "Error") {
              Swal.fire("Error :(", "Alguno de los algoritmos de recomendación ha fallado.", "error");
          } else {
              $('#algorithm_comparison').html('')
              $('#algorithm_comparison').append(content)
          }
      })
  });
});