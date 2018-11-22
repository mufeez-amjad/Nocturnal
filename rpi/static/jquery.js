$(document).ready(function () {

  req = $.ajax({
    url : '/update',
    type : 'POST',
    data
  });

  req.done(function(data) {
    


  });
});