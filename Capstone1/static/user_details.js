$(document).ready(function(){
    //set up event listener on satellite cards
   $('.satellite-container').click(function(evt) {
    let satelliteId = $(this).find('p').attr('id');

    if ($(this).hasClass('text-bg-secondary')){
        removeFromDatabase(satelliteId, this)
    }else{
        addToDatabase(satelliteId, this);
    }
    
   });
   //set an event listener on address cards
   $('.address-container').click(function(evt) {
    if ($(this).hasClass('text-bg-secondary')){
        $(this).removeClass('text-bg-secondary')
    }else{
        $(this).addClass('text-bg-secondary');
    }
    
   });

   //prepopulate already selected cards and turn them gray
   $.ajax({
    url: '/get_user_satellites',
    type: 'GET',
    success: function(satellites) {
        console.log(satellites)
        satellites.forEach(function(satelliteId) {
            let $element = $('p[id="' + satelliteId + '"]');

            $element.parent().parent().addClass('text-bg-secondary'); // Change the class of the selected elements
        });
    },
    error: function(xhr, status, error) {
        console.log('Error fetching user satellites');
    }
    }); 
});

function addToDatabase(satelliteId, callingElement) {
   $.ajax({
       url: '/add_satellite',
       type: 'POST',
       contentType: 'application/json',
       data: JSON.stringify({ satelliteId: satelliteId }),
       success: function(response) {
           $(callingElement).addClass('text-bg-secondary')
       },
       error: function(xhr, status, error) {
           alert(`Error adding satellite ${satelliteId}`);
       }
   });
}
function removeFromDatabase(satelliteId, callingElement) {
    $.ajax({
        url: '/remove_satellite',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ satelliteId: satelliteId }),
        success: function(response) {
            $(callingElement).removeClass('text-bg-secondary')
        },
        error: function(xhr, status, error) {
            alert(`Error removing satellite ${satelliteId}`);
        }
    });
 }

