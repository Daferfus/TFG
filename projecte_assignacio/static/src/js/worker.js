// Waits for any activity from the page
self.onmessage = function(status_url, nanobar, div) {
  console.log(status_url);
  console.log(nanobar);
  console.log(div);
  if(e.data !== undefined) {
    console.log(e.data);
    $.getJSON(status_url, function(data) {
      console.log(data);
  //     // update UI
  //     percent = parseInt(data['current'] * 100 / data['total']);
  //     nanobar.go(percent);
  //     $(status_div.childNodes[1]).text(percent + '%');
  //     $(status_div.childNodes[2]).text(data['status']);
  //     if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
  //         if ('result' in data) {
  //             // show result
  //             $(status_div.childNodes[3]).text('Result: ' + data['result']);
  //         }
  //         else {
  //             // something unexpected happened
  //             $(status_div.childNodes[3]).text('Result: ' + data['state']);
  //         }
  //     }
  //     else {
  //         // rerun in 2 seconds
  //         setTimeout(function() {
  //             update_progress(status_url, nanobar, status_div);
  //         }, 2000);
  //     }
    });
  }
}
// Terminate with: worker.terminate()