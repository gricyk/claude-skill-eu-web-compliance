// Simple cookie notice
(function () {
  if (document.cookie.indexOf("cookie_notice=accepted") !== -1) return;

  var banner = document.createElement("div");
  banner.className = "cookie-banner";
  banner.innerHTML =
    '<p>This website uses cookies to give you the best experience.</p>' +
    '<button id="cookie-accept">Accept all</button> ' +
    '<a class="settings" href="/privacy.html">Settings</a>';
  document.body.appendChild(banner);

  document.getElementById("cookie-accept").addEventListener("click", function () {
    document.cookie = "cookie_notice=accepted; max-age=31536000; path=/";
    banner.remove();
  });
})();
