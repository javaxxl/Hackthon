/**
 * Format returned email in order for rich presentation on the web browser.
 */
var formatID = (value) => {
	return value;
};

var formatSubject = (value) => {
	return value;
};

var formatBody = (value) => {
	return value;
};

var formatSender = (value) => {
	return value;
};

var formatCCList = (value) => {
	return value;
};

var formatSenderRole = (value) => {
	return value;
};

var formatSadness = (value) => {
	return value;
};

var formatJoy = (value) => {
	return value;
};

var formatFear = (value) => {
	return value;
};

var formatDisgust = (value) => {
	return value;
};

var formatAnger = (value) => {
	return value;
};

var formatKeywords = (value) => {
	return value;
};

var formatReceivedTMS = (value) => {
	// The input value is a time stamp type in java, whose format is milliseconds.
	return new Date(value).toString();
};

var formatSentimentScore = (value) => {

	// Determine priority
	if (value >= -1 && value <= -0.5) {
		return '1';
	}
	else if (value > -0.5 && value <= 0) {
		return '2';
	}
	else if (value > 0 && value <= 0.5) {
		return '3';
	}
	else if (value > 0.5 && value <= 1) {
		return '4';
	}
	else {
		// Return no data char when invalid score is discovered.
		return '-';
	}
};

var formatColumn = (value) => {

	let style = { classes: 'format-priority-column' };

	if (value >= -1 && value <= -0.5) {
		style['css'] = { "background-color": "#FF0000" };
	}
	else if (value > -0.5 && value <= 0) {
		style['css'] = { "background-color": "#FF7F50" };
	}
	else if (value > 0 && value <= 0.5) {
		style['css'] = { "background-color": "#FFA07A" };
	}
	else if (value > 0.5 && value <= 1) {
		style['css'] = { "background-color": "#FFDAB9" };
	}
	else {
		style['css'] = { "background-color": "white" };
	}

	return style;
};

/**
 * Define detail view format.
 * @param {*} index is row number.
 * @param {*} row is row contents.
 */

var formatDetail = (index, row) => {
	// Display the email body in detail view.
	return (
		// The outer div to control the overall direction.
		'<div>' +
		// The div to hold the email details.
		'<div id="email-detail' + index + '" class="email-detail-div">' +
		'<p><b>Sent from: </b></p>' +
		'<p>' + row.sender + '</p>' +
		'<p><b>CC to: </b></p>' +
		'<p>' + row.cclist + '</p>' +
		'<p><b>Contents: </b></p>' +
		'<p>' + row.body + '</p>' +
		'</div>' +
		// The div to hold the pie chart.
		'<div id="email-chart' + index + '" class="email-echart-div">' +
		'<div>' +
		// End of the outer div.
		'</div>'
	);
};