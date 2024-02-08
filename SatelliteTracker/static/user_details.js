$(document).ready(function(){
    //set up event listener on satellite cards
   $('.satellite-container').click(function(evt) {
        let satelliteId = $(this).find('p').attr('id');

        if ($(this).hasClass('text-bg-secondary')){
            removeUserSatelliteFromDatabase(satelliteId, this)
        }else{
            addUserSatelliteToDatabase(satelliteId, this);
        }
   });

   //set an event listener on address cards for making address active
   $('.address-list').on('click', '.address-container', function(evt) {
        if ($(this).hasClass('text-bg-secondary')){
            //clicking the active card does nothing
        }else{
            let addressId = $(this).data("address-id");
            $.ajax({
                url: '/make_address_active',
                type: 'POST',
                data: JSON.stringify({addressId : addressId}),
                contentType: 'application/json',
            
                success: function() {
                    console.log("successfully clicked an address")
                },
                error: function(xhr, status, error) {
                    console.log('something went wrong');
                }
                });
            $('.text-bg-secondary').removeClass('text-bg-secondary');
            $(this).addClass('text-bg-secondary');
        }
   });

   //set an event listener on the add address submit button form
   $('#address_submit').click(function(evt){
        evt.preventDefault();
        let addressData = {
            street : $('#street').val(),
            city : $('#city').val(),
            state : $('#state').val(),
            zip : $('#zip').val()
        };
        console.log(JSON.stringify(addressData))
 
        $.ajax({
            url: '/add_address',
            type: 'POST',
            data: JSON.stringify(addressData),
            contentType: 'application/json',
            success: function(resp){
                let addressId = resp[0].address_id
                add_address_card(addressData, addressId);
                //clear the form for the next address
                $('#street').val('');
                $('#city').val('');
                $('#state').val('');
                $('#zip').val('');
            },
            error: function(){
                console.log("Error!  you shit the closet!")
            }
            
        })
   });
   //set up an event listener on the address remove icon
   $('#address-row').on('click', '.fa-xmark', function(evt){

        let row = $(this).closest(".row")
        let addressId = $(this).data("address-id");
        $.ajax({
            url:'/remove_address',
            type:'POST',
            data: JSON.stringify({ addressId: addressId }),
            contentType: 'application/json',
            success:function(){
                row.remove()
            },
            error: function(){
                alert("something went wrong")
            }
        })
        
   });

   //set up a listener on the viewings section of the page.  
   $('#viewings-tab').on('click', function(){
        $.ajax({
            url:'/get_viewings',
            type:'GET',
            success: function(resp){
                console.log(resp.viewings)
                let $header = $('#viewings-header')
                $header.text(`Showing Viewings for: ${resp.address}`)
                let $row = $('#viewings-row')
                $row.empty()  //clear the previous cards 
                resp.viewings.forEach(function(viewing){
                    $row.append(add_viewing_card(viewing))
                })
            },
            error: function(){
                console.error("there was a problem with one of the viewings")
            }
        })
   })

   //prepopulate already selected satellite cards and turn them gray
   $.ajax({
    url: '/get_user_satellites',
    type: 'GET',

    success: function(satellites) {
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

function add_viewing_card(viewingJSON){
    
    let htmlContent = `
      <div class="card col-6">
        <div class="card-body p-2">
          <p class="m-1">${viewingJSON.satellite}</p>
          <p class="m-1">${viewingJSON.date}</p>
          <p class="m-1">visible: ${viewingJSON.visible}</p>
          <p class="m-1">appears: ${viewingJSON.appears} at ${viewingJSON.rise}</p>
          <p class="m-1">dissappears: ${viewingJSON.dissappears}</p>
        </div>
      </div>
    `
    return htmlContent
}

function add_address_card(addressJSON, addressId){
    let $row = $('#address-row')
    let htmlContent = `
    <div class="row">
      <div class="card col-6 address-container" data-address-id="${addressId}">
        <div class="card-body p-2">
          <p class="m-1"> ${addressJSON.street}</p>
          <p class="m-1">${addressJSON.city}, ${addressJSON.state} ${addressJSON.zip}</p>
        </div>
      </div>
      <div class="col-1">
        <i class="fa-solid fa-xmark align-items-center text-danger" data-address-id="${addressId}"></i>
      </div>
    </div>
    `;
    $row.append(htmlContent)
}

function addUserSatelliteToDatabase(satelliteId, callingElement) {
   $.ajax({
       url: '/add_satellite',
       type: 'POST',
       contentType: 'application/json',
       data: JSON.stringify({ satelliteId: satelliteId }),
       success: function(response) {
           $(callingElement).addClass('text-bg-secondary')
       },
       error: function(xhr, status, error) {
           console.error(`there was a problem adding a satellite ${satelliteId}` )
       }
   });
}
function removeUserSatelliteFromDatabase(satelliteId, callingElement) {
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

