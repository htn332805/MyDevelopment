// MathJax configuration for LaTeX rendering in quiz questions
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    packages: {'[+]': ['ams', 'newcommand', 'configmacros']}
  },
  options: {
    menuOptions: {
      settings: {
        zoom: 'NoZoom'  // Disable zoom for cleaner UI
      }
    }
  },
  startup: {
    ready: () => {
      console.log('MathJax is loaded and ready for quiz questions');
      MathJax.startup.defaultReady();
      
      // Add custom function to re-render math after content updates
      window.renderMathJax = function() {
        if (window.MathJax && window.MathJax.typesetPromise) {
          MathJax.typesetPromise().catch(function (err) {
            console.error('MathJax rendering error:', err);
          });
        }
      };
    }
  }
};

// Load MathJax from CDN
(function () {
  var script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
  script.async = true;
  document.head.appendChild(script);
})();