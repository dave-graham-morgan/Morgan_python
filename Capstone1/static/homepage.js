$(document).ready(function(){
   $.ajax({
      url: '/get_apod',
      type: 'GET',
      contentType: 'application/json',
      success: function(resp){
          console.log(resp)
          showAPOD(resp)
      },
      error: function(){
         console.log("something went wrong")
          //TODO: use static image
      }
      
  })


  function showAPOD(resp){
      $hero = $('#home')
      let backgroundUrl = resp.url
      console.log(backgroundUrl)
      $hero.css('background-image', 'url(' + backgroundUrl + ')')
  }

})

