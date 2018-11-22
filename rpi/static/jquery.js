$(document).ready(function() {

  setInterval(function() {
    $.ajax({
        url : '/update',
        type : 'POST',
    }).done(function(data) {
        // $('#sleepCycleGraph').fadeOut(500).fadeIn(500);
        //$('#memberNumber'+member_id).text(data.member_num);
        $('#sleepCycleGraph').html(data);
    });
  }, 1000*60);
  
});