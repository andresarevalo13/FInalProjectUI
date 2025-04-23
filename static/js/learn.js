$(document).ready(function(){
  console.log('learn.js loaded');
  $('#revealBtn').on('click', function(){
    console.log('Reveal button clicked');
    $('#answerPopover').fadeIn();
  });
  $('#nextBtn').on('click', function(){
    var next = $(this).data('next');
    if(next !== undefined) {
      window.location = '/learn/' + next;
    } else {
      window.location = '/home';
    }
  });
});
