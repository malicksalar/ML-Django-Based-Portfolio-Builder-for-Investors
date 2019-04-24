var url = "FinalData.xlsx";
var oReq = new XMLHttpRequest();
oReq.open("GET", url, true);
oReq.responseType = "arraybuffer";

oReq.onload = function(e) {
  var arraybuffer = oReq.response;

  /* convert data to binary string */
  var data = new Uint8Array(arraybuffer);
  var arr = new Array();
  for(var i = 0; i != data.length; ++i) arr[i] = String.fromCharCode(data[i]);
  var bstr = arr.join("");

  /* Call XLSX */
  var workbook = XLSX.read(bstr, {type:"binary"});

  /* DO SOMETHING WITH workbook HERE */
  var first_sheet_name = workbook.SheetNames[0];
  /* Get worksheet */
  var worksheet = workbook.Sheets[first_sheet_name];
  var data = XLSX.utils.sheet_to_json(worksheet,{raw:true})

  var ground = []; // Initialize array
  var returns = [];
  var value_of_return = 0;
  var value_of_volatility = 0;
  var volatile = [];

  var bonds = 0;
  var amount = 0;

  for (var i = data.length; i > data.length - 4; i--) {
    if (i == data.length - 2) {
      returns.push(data[i-1]['Companies']);
      value_of_return = data[i-1]['Portfolio'];
      returns.push(data[i-1]['Portfolio'].toFixed(2) * 100);
    }
    else if (i == data.length - 1) {
      volatile.push(data[i-1]['Companies']);
      value_of_volatility = data[i-1]['Portfolio'];
      volatile.push(data[i-1]['Portfolio'].toFixed(2) * 100);
    }
    else if (i == data.length - 3) {
      bonds = data[i-1]['Portfolio'];
    }
    else if (i == data.length) {
      amount = data[i-1]['Portfolio'];
    }
  }

  for (var i = 0 ; i <= data.length - 3; i++) {
    ground[i] = []; // Initialize inner array
    for (var j = 0; j < 2; j++) {
      if (i == 0){
        ground[i][0] = 'Companies';
        ground[i][1] = 'Values';
      }
      else {
        if (i == data.length - 3) {
          ground[i][0] = data[i-1]['Companies'];
          ground[i][1] = (data[i-1]['Portfolio']);
        }
        else {
          ground[i][0] = data[i-1]['Companies'];
          ground[i][1] = (data[i-1]['Portfolio']) * (1 - bonds);
        }
      }
    }
  }

  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {

    var data1 = google.visualization.arrayToDataTable(ground);
    var options = {
      title: 'Financial Distribution',
      pieHole: 0.4,
    };
    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data1, options);


    var data2 = google.visualization.arrayToDataTable(area_graph);
    var options = {
      title: 'Prediction',
      hAxis: {title: 'Month',  titleTextStyle: {color: '#333'}},
      vAxis: {minValue: amount - (amount * 0.1)}

    };
    var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data2, options);
  }

  var now = [];
  var if_high = [];
  var if_low = [];
  var expected = [];
  var area_graph = []

  for (var i = 0; i < 13; i++) {
    now.push(amount);
  }

  for (var i = 0; i < 13; i++) {
    expected.push(amount + ((value_of_return/12) * i * amount));
  }

  for (var i = 0; i < 13; i++) {
    if_high.push(amount + (((value_of_return + value_of_volatility)/12) * i * amount));
  }

  for (var i = 0; i < 13; i++) {
    if_low.push(amount + (((value_of_return - value_of_volatility)/12) * i * amount));
  }

  for (var i = 0; i < 13; i++) {
    if (i == 0){
      area_graph[i] = [];
      area_graph[i].push('Month');
      area_graph[i].push('Saved');
      area_graph[i].push('Max Profit');
      area_graph[i].push('Min Profit');
      area_graph[i].push('Expected Profit');
    }
    else {
      area_graph[i] = [];
      area_graph[i].push(i)
      area_graph[i].push(now[i]);
      area_graph[i].push(if_high[i]);
      area_graph[i].push(if_low[i]);
      area_graph[i].push(expected[i]);
    }
  }





  all_comps = [];
  temp_name = '';
  temp_val = 0;
  for (var i = 0; i < data.length - 3; i++) {
    data[i]['Portfolio'] = (data[i]['Portfolio'] * amount).toFixed(0);
    temp_val = data[i]['Portfolio'];
    temp_name = data[i]['Companies'];
    all_comps.push(temp_name + '  -  ' + 'Rs ' + temp_val.toString());
  }


  var ret = returns.join('  =  ');
  ret = ret + '%';
  var volt = volatile.join('  =  ');
  volt = volt + '%';
  document.getElementById("returns1").innerHTML = ret;
  document.getElementById("returns2").innerHTML = volt;

  for (var i = 0, j = all_comps.length; i < j; i++) {
    all_comps[i] = '<p>' + all_comps[i] + '</p>'
  }
  document.getElementById("returns3").innerHTML= all_comps.join('')
}

oReq.send();
