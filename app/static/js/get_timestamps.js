// Source: https://stackoverflow.com/questions/1801499/how-to-change-options-of-select-with-jquery
(function($, window) {
  $.fn.replaceOptions = function(options) {
      var self, $option;

      this.empty();
      self = this;

      $.each(options, function(index, option) {
          $option = $("<option></option>")
              .attr("value", option.value)
              .text(option.text);
          self.append($option);
      });
  };
})(jQuery, window);


  $(document).ready(function() {
    $('#selectUser').change(function() {
        // Llamamos a la API con AJAX
        if (this.value != '') {
            $.get('http://localhost:8002/timestamp/?user_id=' + this.value, function(data) {}).done(function(data) {
                // Comportamiento EXITO
                var i;
                var options = [];
                for (i = 0; i < data.length; i++) {
                    options.push({
                        text: data[i],
                        value: i
                    })
                }
                $("#selectTimestamp").replaceOptions(options);
            }).fail(function(data, textStatus, xhr) {
                // Comportamiento ERROR
                $("#selectUser").val('');
                Swal.fire("Error :(", "No hemos podido encontrar al usuario introducido", "error");
            })
        }
    });
})
  
