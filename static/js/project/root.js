$(() => {
  $.ajax({

    url: url + "student",
    type: 'GET',
    dataType: 'json',
    success: function (data) {

      Object.values(data).forEach((row) => {
        let navitem = `<li class="nav-item"> <a class="nav-link" href="${url}faces/${row.id}">${row.nama}</a></li>`;
        $('#student ul').append(navitem);
      })
    },
    error: function (request, error) {
      console.log("Request: " + JSON.stringify(request));
    }
  });
})
