/*global setTimeout */
var debug = false;
function log(s) {
  if (debug) {
    console.log(s);
  }
}

function dom_loaded() {
  return new Promise((resolve, reject) => {
    function listener() {
      log('DOMContentLoaded');
      document.removeEventListener('DOMContentLoaded', listener);
      resolve();
    }
    document.addEventListener('DOMContentLoaded', listener, false);
  });
}

function get_wifi_signal() {
  log('get_wifi_signal');
  return new Promise((resolve, reject) => {
    var req = new XMLHttpRequest();
    req.responseType = 'json';
    req.onload = () => { log('Got wifi signal'); resolve(req.response); };
    req.onerror = (e) => reject(e);
    req.open('GET', '/wifisignal/192.168.1.200', true);
    req.send(null);
  });
}

function fill_wifi_signal(data) {
  log('fill_wifi_signal');
  if (data.signal != null) {
    document.getElementById('wifisignal').value = Math.min(Math.max(data.signal, -100), -60);
    document.getElementById('wifisignalvalue').innerText = data.signal;
  }
}

function set_refresh_timer() {
  log('set_refresh_timer');
  setTimeout(() => get_wifi_signal()
             .then(fill_wifi_signal)
             .then(set_refresh_timer)
             .catch((e) => console.error(e)),
             1000);
}

Promise.all([
  get_wifi_signal(),
  dom_loaded(),
]).then((data) => {
  fill_wifi_signal(data[0]);
  set_refresh_timer();
});
