
$(function () {


  // load image on modal
  let owl = $('.carrou').owlCarousel({
    loop: true,
    margin: 10,
    items: 1,
    nav: false,
    autoplay: true,
    autoplayTimeout: 5500,
  });

  $('#students-face img').on('click', function (e) {
    e.stopImmediatePropagation()
    e.preventDefault()
    $('#table-specify tbody').html('')
    let image_id = $(this).attr('code')
    let img_src = $(this).attr('src');
    let keypoint_src = $(this).attr('keypoint_src')
    let gray = $(this).attr('gray')
    let landmark = $(this).attr('landmark')
    $('#modal-detail_face .original').attr('src', img_src);
    $('#modal-detail_face .keypoint').attr('src', keypoint_src);
    $('#modal-detail_face .gray').attr('src', gray);
    $('#modal-detail_face .landmark').attr('src', landmark);

    let current_data = data[parseInt(image_id)]
    let similar_face = current_data.similar_image_of_label;
    $('#similar-face').html('')

    let label = current_data.identification_accuracy
    if (current_data.label != 'Tidak Diketahui') {
      $('#similar-face').parent().show()
      label = label + "%"
      similar_face.forEach(filename => {
        $('#similar-face').append(
          '<img src="' + asset_url + filename + '" alt="" class="similar-face">'
        )
      });
    }else{
      $('#similar-face').parent().hide()
    }




    $('#identification-time').html(current_data.identification_time)
    $('#identification h3 .result').html(current_data.label)
    $('#identification h3 .loc').html(label)
    $('#orb-time').html(current_data.orb_time)
    $('#keypoint-found').html(current_data.keypoint_found)
    $('#similarity').html(current_data.average_similarity)
    $('#modal-detail_face').modal('show')

    current_data.comparation_image.forEach((row, key) => {
      let similarity = row.similarity * 100
      similarity = Math.round(similarity)
      let bg = ''
      if (similarity > 75) {
        bg = "bg-success"
      } else if (similarity > 50) {
        bg = 'bg-warning';
      } else {
        bg = 'bg-danger'
      }
      $('#table-specify tbody').append(
        `<tr>
        <td class="text-center">`+ (parseInt(key) + 1) + `</td>
        <td>
          <div class="d-flex ">
            <div>
              <h6>`+ row.comparation_label + `</h6>
              <p>ORB Face Identification</p>
            </div>
          </div>
        </td>
        <td>
        <img src="`+ asset_url + row.file_name + `" alt="" style="width: 70%; border-radius:none">
        </td>
        <td>
        <img src="`+ asset_url + row.file_name2 + `" alt="" style="width: 70%; border-radius:none"></td>
        <td>
          <div>
            <div class="d-flex justify-content-between align-items-center mb-1 max-width-progress-wrap">
              <p class="text-successz">`+ similarity + `%</p>
            </div>
            <div class="progress progress-md">
              <div class="progress-bar `+ bg + `" role="progressbar" style="width: ` + similarity + `%" aria-valuenow="25"
                aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
        </td>
        <td>
        <div class="text-center">
          <h6>`+ row.keypoint_match + `</h6>
          <p>Match</p>
      </div>
        </td>
        <td class="text-center">
          <div class="badge badge-opacity-warning">`+ row.execution_time + `s</div>
        </td>
      </tr>`
      )
    });

    $('.modal img').each(function () {
      let img = $(this);
      viewer = new Viewer(img[0], {
        toolbar: false,
      })
    })

  })
})