// Vehicle count bar indicator js
jQuery("#veh_count").radialProgress("init", {
  'size': 100,
  'fill': 5
}).radialProgress("to", {'perc': 10, 'time': 10000});

var temp_meter;
$(document).ready(function() {  
  // Data table plugin	
	$('#alpr_data_tbl').DataTable({    
		"lengthMenu": [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],    
		responsive: true
	});

});

$('#btngetAnalyticsdata').click(function(){
  var STARTDATETIME = $('#anaFromDate').val().replace(/[.]/g, '-');  
  var ENDDATATIME = $('#anaToDate').val().replace(/[.]/g, '-');
  createAnalyticsTable(null, STARTDATETIME, ENDDATATIME, null);
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
    $('#alpr-parking-hours').text($.trim(tableData[10]));
    $('#alpr-total-cost').text($.trim(tableData[12]));
    $('#alpr_image').attr('src', $.trim(tableData[2]));
    $('#alpr_veh_image').attr('src', $.trim(tableData[3]));
    $('#alpr_qrcode_image').attr('src', $.trim(tableData[4]));

    console.log("Your data is: " + $.trim(tableData[0]) + " , " + $.trim(tableData[1]) + " , " + $.trim(tableData[2]));
  });
});
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
      console.log(rows_count)
      amount_meter.refresh(total_cost);
      park_hrs_meter.refresh(total_park_hours);
      console.log(data_table);
      if(flag==='CURRENT'){
        $.each(data_table, function(i, value){                      
          $("#alpr_data_tbl").append("<tr class='alpr-data-tr' id='alpr-data-tr' data-toggle='modal' data-target='#myTrDataModal' ><td>"+value.ALPR_ID+"</td><td><img src="+value.ALPR_IMG+" height='50px' width='100px'></td><td><img src='"+value.VEHICLE_IMG+"' height='50px' width='100px'></td><td><img src='"+value.QRCODE_IMG+"' height='50px' width='50px'></td><td>"+value.STARTDATETIME+"</td><td>"+value.ENDDATATIME+"</td><td>"+value.PARKING_HOURS+"</td><td>"+value.TOTAL_COST+"</td></tr>");
        });
      }else{        
        $.each(data_table, function(i, value){                      
          $("#alpr_data_tbl").append("<tr class='alpr-data-tr' id='alpr-data-tr' data-toggle='modal' data-target='#myTrDataModal' ><td>"+value.ALPR_ID+"</td><td><img src="+value.ALPR_IMG+" height='50px' width='100px'></td><td><img src='"+value.VEHICLE_IMG+"' height='50px' width='100px'></td><td><img src='"+value.QRCODE_IMG+"' height='50px' width='50px'></td><td>"+value.STARTDATETIME+"</td><td>"+value.ENDDATATIME+"</td><td>"+value.PARKING_HOURS+"</td><td>"+value.TOTAL_COST+"</td></tr>");
        });
        console.log(rows_count);            
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

function check(e)
{
  e.preventDefault();
  return false;
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