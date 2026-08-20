document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('video').forEach(function(video) {
    video.defaultPlaybackRate = 1.0;
    video.playbackRate = 1.0;
  });

  document.querySelectorAll('[data-video-highlight]').forEach(function(highlight) {
    var mainVideo = highlight.querySelector(':scope > video');
    var detailVideo = highlight.querySelector('.contact-detail-inset video');

    if (!mainVideo || !detailVideo) {
      return;
    }

    function syncDetailTime() {
      if (Math.abs(detailVideo.currentTime - mainVideo.currentTime) > 0.12) {
        detailVideo.currentTime = mainVideo.currentTime;
      }
    }

    mainVideo.addEventListener('play', function() {
      syncDetailTime();
      detailVideo.playbackRate = mainVideo.playbackRate;
      detailVideo.play().catch(function() {});
    });

    mainVideo.addEventListener('pause', function() {
      detailVideo.pause();
    });

    mainVideo.addEventListener('seeking', syncDetailTime);
    mainVideo.addEventListener('timeupdate', syncDetailTime);
    mainVideo.addEventListener('ratechange', function() {
      detailVideo.playbackRate = mainVideo.playbackRate;
    });

    if (mainVideo.paused) {
      detailVideo.pause();
    } else {
      syncDetailTime();
    }
  });

  document.querySelectorAll('[data-video-carousel]').forEach(function(carousel) {
    var slides = Array.from(carousel.querySelectorAll('[data-carousel-slide]'));
    var pageButtons = Array.from(carousel.querySelectorAll('[data-carousel-page]'));
    var activeIndex = 0;
    var touchStartX = 0;
    var touchStartY = 0;

    function showSlide(nextIndex, restartVideo) {
      activeIndex = (nextIndex + slides.length) % slides.length;

      slides.forEach(function(slide, index) {
        var isActive = index === activeIndex;
        slide.hidden = !isActive;

        slide.querySelectorAll('video').forEach(function(video) {
          if (!isActive) {
            video.pause();
            return;
          }

          if (restartVideo) {
            try {
              video.currentTime = 0;
            } catch (error) {}
          }

          if (!carousel.closest('[hidden]')) {
            video.play().catch(function() {});
          }
        });
      });

      pageButtons.forEach(function(button, index) {
        var isActive = index === activeIndex;
        button.classList.toggle('is-active', isActive);
        button.setAttribute('aria-pressed', String(isActive));
      });
    }

    pageButtons.forEach(function(button) {
      button.addEventListener('click', function() {
        showSlide(Number(button.dataset.carouselPage), true);
      });
    });

    carousel.addEventListener('touchstart', function(event) {
      var touch = event.changedTouches[0];
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
    }, { passive: true });

    carousel.addEventListener('touchend', function(event) {
      var touch = event.changedTouches[0];
      var deltaX = touch.clientX - touchStartX;
      var deltaY = touch.clientY - touchStartY;

      if (Math.abs(deltaX) < 50 || Math.abs(deltaX) <= Math.abs(deltaY)) {
        return;
      }

      showSlide(activeIndex + (deltaX < 0 ? 1 : -1), true);
    }, { passive: true });

    showSlide(0, false);
  });

  document.querySelectorAll('[data-task-switcher]').forEach(function(switcher) {
    var tabs = switcher.querySelectorAll('.task-tab');
    var panels = switcher.querySelectorAll('.task-panel');

    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        var targetId = tab.dataset.taskTarget;

        tabs.forEach(function(candidate) {
          var isActive = candidate === tab;
          candidate.classList.toggle('is-dark', isActive);
          candidate.setAttribute('aria-selected', String(isActive));
        });

        panels.forEach(function(panel) {
          var isActive = panel.id === targetId;
          panel.hidden = !isActive;

          panel.querySelectorAll('video').forEach(function(video) {
            if (isActive && !video.closest('[hidden]')) {
              video.play().catch(function() {});
            } else {
              video.pause();
            }
          });
        });
      });
    });
  });
});
