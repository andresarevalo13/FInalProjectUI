// $(document).ready(function(){
//   console.log('learn.js loaded');
//   $('#revealBtn').on('click', function(){
//     console.log('Reveal button clicked');
//     $('#answerPopover').fadeIn();
//   });
//   $('#nextBtn').on('click', function(){
//     var next = $(this).data('next');
//     if(next !== undefined) {
//       window.location = '/learn/' + next;
//     } else {
//       window.location = '/home';
//     }
//   });
// });

//  $(document).ready(function () {
//   console.log('learn.js loaded');

//   $('#revealBtn').on('click', function () {
//     $('#answerBlock').show();
//     $(this).prop('disabled', true);
//   });

//   $('#nextBtn').on('click', function () {
//     const next = $(this).data('next');
//     if (next !== undefined) {
//       window.location = '/learn/' + next;
//     } else {
//       window.location = '/';
//     }
//   });

//   // Slider logic
//   const container = document.getElementById('comparison-container');
//   const slider = document.getElementById('slider');
//   const resize = document.getElementById('resize');

//   if (container && slider && resize) {
//     let isDragging = false;

//     const startDrag = () => { isDragging = true; };
//     const endDrag = () => { isDragging = false; };
//     const onDrag = (e) => {
//       if (!isDragging) return;
//       const rect = container.getBoundingClientRect();
//       let x = e.clientX - rect.left;
//       x = Math.max(0, Math.min(x, rect.width));
//       resize.style.width = x + 'px';
//       slider.style.left = x + 'px';
//     };

//     slider.addEventListener('mousedown', startDrag);
//     window.addEventListener('mouseup', endDrag);
//     window.addEventListener('mousemove', onDrag);
//   }
//  });
$(document).ready(function () {
  const container = document.getElementById("comparison-container");
  const slider = document.getElementById("slider");
  const resize = document.getElementById("resize");

  if (container && slider && resize) {
    let isDragging = false;

    const startDrag = (e) => {
      isDragging = true;
      e.preventDefault();
    };

    const stopDrag = () => {
      isDragging = false;
    };

    const onDrag = (e) => {
      if (!isDragging) return;

      const rect = container.getBoundingClientRect();
      let x = e.clientX - rect.left;

      // Clamp x between 0 and container width
      x = Math.max(0, Math.min(x, rect.width));

      resize.style.width = x + "px";
      slider.style.left = x + "px";
    };

    slider.addEventListener("mousedown", startDrag);
    window.addEventListener("mouseup", stopDrag);
    window.addEventListener("mousemove", onDrag);

    // For mobile/touch support (optional)
    slider.addEventListener("touchstart", startDrag);
    window.addEventListener("touchend", stopDrag);
    window.addEventListener("touchmove", (e) => {
      if (!isDragging || !e.touches.length) return;

      const rect = container.getBoundingClientRect();
      let x = e.touches[0].clientX - rect.left;
      x = Math.max(0, Math.min(x, rect.width));
      resize.style.width = x + "px";
      slider.style.left = x + "px";
    });
  }
});
