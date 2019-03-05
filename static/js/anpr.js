function refreshimage(node)
{
   var times = 3000; // gap in Milli Seconds;

   (function startRefresh()
   {
      var address;
      if(node.src.indexOf('?')>-1)
       address = node.src.split('?')[0];
      else 
       address = node.src;
      node.src = address+"?time="+new Date().getTime();

      //setTimeout(startRefresh,times);
   })();

}
function printDiv(divID) {
    //Get the HTML of div
    var divElements = document.getElementById(divID).innerHTML;
    //Get the HTML of whole page
    var oldPage = document.body.innerHTML;
    //Reset the page's HTML with div's HTML only
    document.body.innerHTML = "<html><head><title></title></head><body>"+divElements+"</body>";
    //Print Page
    window.print();
    //Restore orignal HTML
    document.body.innerHTML = oldPage;     
}

window.onload = drawchart(0 , 0);
  function drawchart(qrcount, vehcount, date) {
    var chart = new CanvasJS.Chart("chartContainer",
    {
      title:{
        text: "Count of Vehicle, Number plates"
      },
      axisY: {
        title: "Vehicles",
        maximum: 100
      },
      data: [
      {
        type: "bar",
        showInLegend: true,
        legendText: "QRcode",
        color: "gold",
        dataPoints: [
        { y: qrcount, label: date}
        ]
      },
      {
        type: "bar",
        showInLegend: true,
        legendText: "Vehicles",
        color: "#DCA978",
        dataPoints: [
        { y: vehcount, label: date}
        ]
      }
      ]
    });

chart.render();
}

function CreateTableFromJSON(message){
    var myBooks = message;
    // EXTRACT VALUE FOR HTML HEADER. 
    // ('Book ID', 'Book Name', 'Category' and 'Price')
    var col = [];
    for (var i = 0; i < myBooks.length; i++) {
        for (var key in myBooks[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    // CREATE DYNAMIC TABLE.
    var table = document.createElement("table");
    table.id = 'tableID';
    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.innerHTML = col[i];
        tr.appendChild(th);
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < myBooks.length; i++) {

        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = myBooks[i][col[j]];
        }
    }

    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    var divContainer = document.getElementById("showData");
    divContainer.innerHTML = "";
    divContainer.appendChild(table);
}

function initCropper(){
      console.log("Came here");
      var image = document.getElementById('livefeed');
      var cropper = new Cropper(image, {
        aspectRatio: 1 / 1,
        crop: function(e) {
          console.log(e.detail.x);
          console.log(e.detail.y);
        }
      });

      // On crop button clicked
      document.getElementById('crop_button').addEventListener('click', function(){
          var imgurl =  cropper.getCroppedCanvas().toDataURL();
          var img = document.createElement("img");
          img.src = imgurl;
          document.getElementById("cropped_result").appendChild(img);

          /* ---------------- SEND IMAGE TO THE SERVER-------------------------

          cropper.getCroppedCanvas().toBlob(function (blob) {
              var formData = new FormData();
              formData.append('croppedImage', blob);
              // Use `jQuery.ajax` method
              $.ajax('/path/to/upload', {
                method: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function () {
                  console.log('Upload success');
                },
                error: function () {
                  console.log('Upload error');
                }
              });
          });
          */
        })
      }