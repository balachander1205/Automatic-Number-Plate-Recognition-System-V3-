var temp_meter;
$(document).ready(function() {  
  
	// Data table plugin	
	$('#alpr_data_tbl').DataTable({
		"lengthMenu": [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
		responsive: true
	});
});

// getting tr data on click row
$(function () {
  $("#alpr_data_tbl").on('click','tr',function() {
    var alpr_modal_data = [];      
    var tableData = $(this).children("td").map(function() {        
      if ($(this).find('img')){
        var alpr_img = $(this).find('img').attr('src');
        alpr_modal_data.push(alpr_img);
      }
      if($(this).text()){
        alpr_modal_data.push($(this).text());                        
      }
      return alpr_modal_data;
    }).get();
    console.log(alpr_modal_data);
    $('#alpr-id').text($.trim(tableData[1]));
    $('#alpr-startdatetime').text($.trim(tableData[6]));
    // $('#alpr-enddatetime').text($.trim(tableData[8]));
    $('.alpr-enddatetime').val($.trim(tableData[8]));
    // $('#alpr-parking-hours').text($.trim(tableData[10]));
    // $('#alpr-total-cost').text($.trim(tableData[12]));
    $('#alpr_image').attr('src', $.trim(tableData[2]));
    $('#alpr_veh_image').attr('src', $.trim(tableData[3]));
    $('#alpr_qrcode_image').attr('src', $.trim(tableData[4]));
    $('#alpr_veh_num').text($.trim(tableData[14]));
    console.log($.trim(tableData[14]));
    
    park_hrs_veh_meter.refresh($.trim(tableData[10]));
    park_hrs_amount_meter.refresh($.trim(tableData[12]));

    console.log("Your data is: " + $.trim(tableData[0]) + " , " + $.trim(tableData[1]) + " , " + $.trim(tableData[2]));
  });
});
//  Updation of record
// Updation of ALPR record
$('#update_alpr_record').click(function() {
  var ALPR_ID = $('#alpr-id').text();
  var STARTDATETIME = $('#alpr-startdatetime').text();
  // var ENDDATATIME = $("#end_date_datepicker").datepicker("getDate");
  var ENDDATATIME = $('#end_date_datepicker').val().replace(/[.]/g, '-');
  // console.log(ENDDATATIME);

  // ENDDATATIME = $.datepicker.formatDate("yy-mm-dd", ENDDATATIME);    
  var d = new Date(),
  hrs = (d.getHours()<10?'0':'') + d.getHours(),
  min = (d.getMinutes()<10?'0':'') + d.getMinutes();
  var hrs_min = hrs + ':' + min;
  ENDDATATIME = ENDDATATIME+" "+hrs_min;
  console.log(ENDDATATIME);     
  $.ajax({
    url: 'http://localhost:5000/updatealprdata?alprid='+ALPR_ID+"&startdatetime="+STARTDATETIME+"&enddatetime="+ENDDATATIME,                
    type: 'POST',
    success: function(response){                             
      var resp = response;
      console.log(resp);          
    },
    error: function(error){
      console.log(error);
    }
  });
});

function printData()
{
  var divToPrint=document.getElementById("veh-qrcode-img");
  newWin= window.open("");
  newWin.document.write(divToPrint.outerHTML);
  newWin.print();
  newWin.close();  
}

$('#print_receipt').on('click',function(){
  printData();
})
// Getting file name from Image src
String.prototype.filename=function(extension){
    var s= this.replace(/\\/g, '/');
    s= s.substring(s.lastIndexOf('/')+ 1);
    return extension? s.replace(/[?#].+$/, ''): s.split('.')[0];
}

//  Imaging croppping css
function cropimage(){
    var image = $('.modal-body>img');      
    image.cropper('destroy');
    var cropper = image.cropper({
      aspectRatio: 16 / 9,
      crop: function(e) {
        console.log(e.x);
        console.log(e.y);
        console.log(e.width);
        console.log(e.height);
        console.log(e.rotate);
        console.log(e.scaleX);
        console.log(e.scaleY);
      }
    });
  // End of cropper on modal window
  // On crop button clicked
    document.getElementById('save-cropped-image').addEventListener('click', function(){
      image.cropper('getCroppedCanvas').toBlob(function (blob) {
        var formData = new FormData();
        var img = document.createElement("img");
        $('#cropped_result').empty();
        $('#cropped_result > img').addClass('croppedimage');
          // converting blob to base64string
          var reader = new window.FileReader();
          reader.readAsDataURL(blob);            
          reader.onloadend = function() {
              base64data = reader.result;                
              img.src = base64data;
              document.getElementById("cropped_result").appendChild(img);
          }              
        });          
    })
}

function cancelCrop(){
  var image = $('.modal-body>img');
  image.cropper('destroy');
}

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

function createAnalyticsTable(date, from_date, to_date, flag) {
  $.ajax({
    url: 'http://localhost:5000/getalprsqltabledata?date='+date+"&fromdate="+from_date+"&todate="+to_date,                
    type: 'POST',
    success: function(response){
      $("#alpr_data_tbl tbody").empty();
      $("#alpr_current_date_data_table tbody").empty(); 
      var resp = response;
      var obj = JSON.parse(resp);                    

      var data_table = JSON.parse(obj.tabledata);

      var rows_count = obj.rowcount;
      var total_cost = obj.totalcost;
      var total_park_hours = obj.totalparkhours;
      veh_count_meter.refresh(rows_count);
      amount_meter.refresh(total_cost);
      park_hrs_meter.refresh(total_park_hours);
      console.log(rows_count);      
      if(flag==='CURRENT'){
        $.each(data_table, function(i, value){                      
          $("#alpr_data_tbl").append("<tr class='alpr-data-tr' id='alpr-data-tr' data-toggle='modal' data-target='#myTrDataModal' ><td>"+value.ALPR_ID+"</td><td><img src="+value.ALPR_IMG+" height='50px' width='100px'></td><td><img src='"+value.VEHICLE_IMG+"' height='50px' width='100px'></td><td><img src='"+value.QRCODE_IMG+"' height='50px' width='50px'></td><td>"+value.STARTDATETIME+"</td><td>"+value.ENDDATATIME+"</td><td>"+value.PARKING_HOURS+"</td><td>"+value.TOTAL_COST+"</td><td>"+value.VEHICLE_NUM+"</td></tr>");
        });
      }else{        
        $.each(data_table, function(i, value){                      
          $("#alpr_data_table").append("<tr class='alpr-data-tr' id='alpr-data-tr' data-toggle='modal' data-target='#myTrDataModal' ><td>"+value.ALPR_ID+"</td><td><img src="+value.ALPR_IMG+" height='50px' width='100px'></td><td><img src='"+value.VEHICLE_IMG+"' height='50px' width='100px'></td><td><img src='"+value.QRCODE_IMG+"' height='50px' width='50px'></td><td>"+value.STARTDATETIME+"</td><td>"+value.ENDDATATIME+"</td><td>"+value.PARKING_HOURS+"</td><td>"+value.TOTAL_COST+"</td><td>"+value.VEHICLE_NUM+"</td></tr>");
        });         
        veh_count_meter.refresh(rows_count);           
        amount_meter.refresh(total_cost);
        park_hrs_meter.refresh(total_park_hours);
      }      
    },
    error: function(error){
      console.log(error);
    }
  });
  // $('#end_date_datepicker').datepicker();
}
function clock(){
  var audioElement = new Audio("");

  //clock plugin constructor
  $('#myclock').thooClock({
    size:$(document).height()/1.4,
    onAlarm:function(){
      //all that happens onAlarm
      $('#alarm1').show();
      alarmBackground(0);
      //audio element just for alarm sound
      document.body.appendChild(audioElement);
      var canPlayType = audioElement.canPlayType("audio/ogg");
      if(canPlayType.match(/maybe|probably/i)) {
        audioElement.src = 'alarm.ogg';
      } else {
        audioElement.src = 'alarm.mp3';
      }
      // erst abspielen wenn genug vom mp3 geladen wurde
      audioElement.addEventListener('canplay', function() {
        audioElement.loop = true;
        audioElement.play();
      }, false);
    },
    showNumerals:true,
    // brandText:'THOOYORK',
    // brandText2:'Germany',
    onEverySecond:function(){
      //callback that should be fired every second
    },
    //alarmTime:'15:10',
    offAlarm:function(){
      $('#alarm1').hide();
      audioElement.pause();
      clearTimeout(intVal);
      $('body').css('background-color','#FCFCFC');
    }
  });
}

$('#do-alpr').click(function () {
  var base64string = $('#cropped_result img').attr('src');
  console.log(base64string);
})
