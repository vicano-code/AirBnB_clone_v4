$(document).ready(function() {
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
});
