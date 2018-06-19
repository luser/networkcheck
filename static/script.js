/*global setTimeout */
var debug = false;
function log(s) {
  if (debug) {
    console.log(s);
  }
}

function get_network_status() {
  log('get_network_status');
  return new Promise((resolve, reject) => {
    var req = new XMLHttpRequest();
    req.responseType = 'json';
    req.onload = () => { log('Got data'); resolve(req.response); };
    req.onerror = (e) => reject(e);
    req.open('GET', '/data', true);
    req.send(null);
  });
}

function get_wifi_signal() {
  log('get_wifi_signal');
  return new Promise((resolve, reject) => {
    var req = new XMLHttpRequest();
    req.responseType = 'json';
    req.onload = () => { log('Got wifi signal'); resolve(req.response); };
    req.onerror = (e) => reject(e);
    req.open('GET', '/wifisignal', true);
    req.send(null);
  });
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

function fill_table(data) {
  log('fill_table');
  var b = document.getElementsByTagName('table')[0].tBodies[0];
  for (var i = 0; i < data.hosts.length; i++) {
    let [host, name, status] = data.hosts[i];
    status = status ? 'UP' : 'DOWN';
    var row = document.getElementById(host);
    if (row) {
      row.cells[1].textContent = status;
      row.cells[1].className = status;
    }
  }
}

function fill_wifi_signal(data) {
  log('fill_wifi_signal');
  for (let {host, signal} of data.hosts) {
    log(`fill_wifi_signal: ${host}, ${signal}`);
    document.getElementById(`wifisignal_${host}`).value = Math.min(Math.max(signal, -100), -60);
    document.getElementById(`wifisignalvalue_${host}`).innerText = signal;
  }
}

function set_refresh_timer() {
  log('set_refresh_timer');
  setTimeout(() => {
    Promise.all([
      get_network_status()
        .then(fill_table),
      get_wifi_signal()
        .then(fill_wifi_signal),
    ]).then(set_refresh_timer)
      .catch((e) => console.error(e));
  }, 30000);
}

Promise.all([
  Promise.all([
    get_network_status(),
    dom_loaded(),
  ]).then((data) => fill_table(data[0])),
  Promise.all([
    get_wifi_signal(),
    dom_loaded(),
  ]).then((data) => fill_wifi_signal(data[0])),
]).then(set_refresh_timer)
  .catch((e) => console.error(e));
