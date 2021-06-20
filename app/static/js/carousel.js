// Source: https://www.codeply.com/go/EIOtI7nkP8/bootstrap-carousel-with-multiple-cards

function reload_carousel() {
  $('#recipeCarousel').carousel({
    interval: 10000
  })
  
  $('.carousel .carousel-item').each(function(){
      var minPerSlide = 3;
      var next = $(this).next();
      if (!next.length) {
      next = $(this).siblings(':first');
      }
      next.children(':first-child').clone().appendTo($(this));
      
      for (var i=0;i<minPerSlide;i++) {
          next=next.next();
          if (!next.length) {
              next = $(this).siblings(':first');
            }
          
          next.children(':first-child').clone().appendTo($(this));
        }
  });
}



 $(document).ready(function() {
    $('#selectUser').change(function() {
      $.get( 'carousel?user_id='+$('#selectUser').val(), function( content ) {
        $('#carouselClicked').html('')
        $('#carouselClicked').append(content)
        })
      });
});



