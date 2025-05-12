$(function(){
  $('#prevBtn').click(function(){ window.location='/rules/'+$(this).data('prev'); });
  $('#nextBtn').click(function(){ window.location='/rules/'+$(this).data('next'); });
  $('#backRules').click(function(){ window.location='/rules'; });
});
