

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
					Temperature: data[0].Temperature,
					Humidity: data[0].Humidity,
					Wind_speed: data[0].Wind_speed};
		console.log(weatherInfo)
		Object.entries(weatherInfo).forEach(([key,value]) => {
			panel.append("h6").text(`${key}: ${value}`);
		})
	});

}

get_owm(selected_city)
