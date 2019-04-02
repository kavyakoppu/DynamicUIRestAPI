function manage(val) {
    var bt = document.getElementById('submit');
    if(val == "") {
        bt.disabled = true;
        $('#displayWeatherInfo').hide()
        $('#dispWForecast').hide()
        $('#dispWForecastSite').hide()
    }
    else if(val == "GetWDates"){
        $('#datediv').hide();
        $('#tmaxdiv').hide();
        $('#tmindiv').hide();
        bt.disabled = false;
        $('#displayWeatherInfo').hide()
        $('#dispWForecast').hide()
        $('#dispWForecastSite').hide()
    }
    else if(val == "GetWDay") {
        $('#datediv').show();
        $('#tmaxdiv').hide();
        $('#tmindiv').hide();
        bt.disabled = false;
        $('#displayWeatherInfo').hide()
        $('#dispWForecast').hide()
        $('#dispWForecastSite').hide()
    }
    else if(val == "AddWDay") {
        $('#datediv').show();
        $('#tmaxdiv').show();
        $('#tmindiv').show();
        bt.disabled = false;
        $('#displayWeatherInfo').hide()
        $('#dispWForecast').hide()
        $('#dispWForecastSite').hide()
    }
    else if(val == "DeleteWDay") {
        $('#datediv').show();
        $('#tmaxdiv').hide();
        $('#tmindiv').hide();
        bt.disabled = false;
        $('#displayWeatherInfo').hide()
        $('#dispWForecast').hide()
        $('#dispWForecastSite').hide()
    }
    else if(val == "Forecast") {
        $('#datediv').show();
        $('#tmaxdiv').hide();
        $('#tmindiv').hide();
        bt.disabled = false;
        $('#displayWeatherInfo').hide()
        $('#dispWForecast').hide()
        $('#dispWForecastSite').hide()
    }
};

baseurl = window.location.href;

const createTable = function(data) {
    var table = document.createElement("table");
   //Add Heading
   var heading = table.createCaption();
   heading.innerHTML = "<b>Weather ForeCast for Week " + data[0].DATE + "</b>";
    //Add a header
    var header = document.createElement("tr");
    var DATEHeaderCell = document.createElement("th");
    var TMAXHeaderCell = document.createElement("th");
    var TMINHeaderCell = document.createElement("th");

    DATEHeaderCell.appendChild(document.createTextNode("DATE"));
    TMAXHeaderCell.appendChild(document.createTextNode("TMAX"));
    TMINHeaderCell.appendChild(document.createTextNode("TMIN"));

    header.appendChild(DATEHeaderCell);
    header.appendChild(TMAXHeaderCell);
    header.appendChild(TMINHeaderCell);

    table.appendChild(header);
    //Add the rest of the data to the table
    for(var i = 0; i < data.length; i++) {
        var date = data[i].DATE;
        var tmax = data[i].TMAX;
        var tmin = data[i].TMIN;

        var tr = document.createElement("tr");

        var dateCell = document.createElement("td");
        var tmaxCell = document.createElement("td");
        var tminCell = document.createElement("td");

        dateCell.appendChild(document.createTextNode(date));
        tmaxCell.appendChild(document.createTextNode(tmax));
        tminCell.appendChild(document.createTextNode(tmin));

        tr.appendChild(dateCell);
        tr.appendChild(tmaxCell);
        tr.appendChild(tminCell);

        table.appendChild(tr);
    }
    return table;
}

$('#submit').click(function(){
    var field = document.getElementById('selectMethod');
    if(field.value == "GetWDates"){ 
        $.get(baseurl+"historical/", function(data) {
            var output = "Weather Information is available for following Dates:\n\n";
            jQuery.each(data, (_index, element)=>{
                output += element.DATE + "\n";
            });
            $("#displayWeatherInfo").val(output);
            $('#displayWeatherInfo').show();
        }, "json");
    }

    if(field.value == "GetWDay"){
        var date = document.getElementById('date');
        var output = "";
        if(!(date.value == undefined || date.value == "")) {
            dateParam = date.value.replace(/-/g, "");
            $.ajax({
                type: 'GET', 
                url: baseurl+"historical/"+dateParam,
                statusCode: { 
                    200: function(data) {
                        // console.log(data);
                        output = "DATE:" + data.DATE + "\n" + "TMAX:" + data.TMAX + "\n" + "TMIN:" + data.TMIN;
                        $("#displayWeatherInfo").val(output);
                        $('#displayWeatherInfo').show();
                    },
                    404: function() {
                        $("#displayWeatherInfo").val("Data for given Date Not Found");
                        $('#displayWeatherInfo').show();
                    }
                }
            });
        }
        else {
            output = "Invalid Date";
            $("#displayWeatherInfo").val(output);
            $('#displayWeatherInfo').show();
        }    
    }
    
    if(field.value == "AddWDay"){
        var date = document.getElementById('date');
        dateParam =  date.value.replace(/-/g , "");
        var tmax = document.getElementById('tmax');
        var tmin = document.getElementById('tmin');
        var senddata = {"DATE": dateParam, "TMAX": tmax.value, "TMIN": tmin.value};
        // console.log(senddata);
        if(!(dateParam == undefined || dateParam == "" || tmax.value == undefined || tmax.value == "" || tmin.value == undefined || tmin.value == "" || tmax.value <= tmin.value)) {
            $.ajax({
                type: 'POST',
                url: baseurl + "historical/",
                contentType: "application/json",
                datatype: "json",
                data: JSON.stringify(senddata),
                statusCode: {
                    201: function() {
                        output = "Added data for DATE:" + senddata.DATE
                        $("#displayWeatherInfo").val(output);
                        $('#displayWeatherInfo').show();
                        
                    },
                    400: function() {
                        $("#displayWeatherInfo").val("Invalid Date");
                        $('#displayWeatherInfo').show();
                    }
                }
            });
        }
        else {
            output = "Invalid Date or Temperature values";
            $("#displayWeatherInfo").val(output);
            $('#displayWeatherInfo').show();
        }    
    }

    if(field.value == "DeleteWDay"){
        var date = document.getElementById('date');
        var output = "";
        if(!(date.value == undefined || date.value == "")) {
            dateParam = date.value.replace(/-/g, "");
            $.ajax({
                type: 'DELETE',
                url: baseurl+"historical/"+dateParam,
                statusCode: {
                    204: function() {
                        output = "Deleted data of :" + dateParam;
                        $("#displayWeatherInfo").val(output);
                        $('#displayWeatherInfo').show(); 
                    },
                    404: function() {
                        $("#displayWeatherInfo").val("Data for given Date Not Found");
                        $('#displayWeatherInfo').show();
                    }
                }
            });
        }
        else {
            output = "Invalid Date";
            $("#displayWeatherInfo").val(output);
            $('#displayWeatherInfo').show();
        }    
    }

    if(field.value == "Forecast") {
        var date = document.getElementById('date');
        
        if(!(date.value == undefined || date.value == "")) {
            dateParam = date.value.replace(/-/g, "");
            $.ajax({
                type: 'GET',
                url: baseurl+"forecast/"+dateParam,
                statusCode: {
                    200: function(data) {
                        const table=createTable(data)
                        document.body.appendChild(table);
                        $('#displayWeatherInfo').hide();
                        $('#dispWForecast').html(table);
                        $('#dispWForecast').show();
                        $('#dispWForecastSite').show();
                    }
                }
            });
        }
        else {
            $("#displayWeatherInfo").html("Invalid Date");
            $('#displayWeatherInfo').show();
        }
    }

});