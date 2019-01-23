

var selected_city = d3.select('#dropdownSelect').node().selectedOptions[0].value;


function get_owm(selected_city) {

	var selected_city = d3.select('#dropdownSelect').node().selectedOptions[0].value;
	//console.log(selected_city)
	
	d3.json(`/weather?selected_city=${selected_city}`).then((data) => {
		//console.log(data[0].City)
		var panel = d3.select("#panel-status");
		panel.html("");
		var weatherInfo = 
					{City: data[0].City,
					Description: data[0].Description,
					Temperature: Number((data[0].Temperature).toFixed(0)),
					Humidity: data[0].Humidity ,
					Wind: data[0].Wind_speed};
		//console.log(weatherInfo)
		Object.entries(weatherInfo).forEach(([key,value]) => {
			panel.append("h6").text(`${key}: ${value}`);
		})
	});
	d3.json(`/prediction?selected_city=${selected_city}`).then((predData) => {
	//console.log(predData[0].Predicted_temp_next_day) 
	var predictedTemp = {Temp_tomorrow: predData[0].Predicted_temp_next_day};
	console.log(predictedTemp)
	Object.entries(predictedTemp).forEach(([key,value]) =>{
		var span = document.getElementById("prediction").innerHTML=`${value}`;
		span.html("")
	})
	});

	var bgImage = {
		Amsterdam: '/static/css/img/ams.jpg',
		Irvine: 'placeholder.jpg',
		Lihue: '/static/css/img/kauai.jpg',
		Kyoto: '/static/css/img/kyoto.jpg',
		Nice: '/static/css/img/stjeannet.jpg',
		Manly: '/static/css/img/manly.jpg',
		Salvador: '/static/css/img/salvador.jpg'
		};
	//Object.entries(bgImage).forEach(([key,value]) => {	
	//var bgBody = document.getElementByTagName("body");

	//})


}

get_owm(selected_city)

