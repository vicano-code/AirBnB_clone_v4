$(document).ready(function() {
  //Display list of checkboxes selected
  let amenityIds = {};
  $('input[type=checkbox]').change(function() {
    let id = $(this).attr('data-id');
    let name = $(this).attr('data-name');
    if ($(this).is(':checked')) {
      amenityIds.id = name;
    } else {
      delete amenityIds[id]
    } 
    $('h4.amenities').text(amenityIds.values().join(', '));
  });

  //display red circle on top-right of page if connection status OK
  $.ajax({
    type: 'GET',
    url: 'http://0.0.0.0:5001/api/v1/status/',
    dataType: 'json',
    success: function (data) {
      if (data.status === 'OK') {
        $('#api_status').addClass('available');
      } else {
        $('#api_status').removeClass('available')
      }
    }
  })
});
