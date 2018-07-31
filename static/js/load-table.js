/*
	The url is actually calling API service: http://localhost:8082/testWatson/
 */
$('#table').bootstrapTable({
	url: 'emails',
	columns: [{
		field: 'state',
		checkbox: true
	},
	{
		field: 'sentimentScore',
		title: 'Priority',
		sortable: true,
		formatter: 'formatSentimentScore',
		// Define column style.
		cellStyle: 'formatColumn'
	}, {
		field: 'senderRole',
		title: 'SenderRole',
		sortable: true,
		formatter: 'formatSenderRole'
	}, {
		field: 'subject',
		title: 'Subject',
		sortable: true,
		formatter: 'formatSubject'
	}, {
		field: 'receievedTimestamp',
		title: 'Received',
		sortable: true,
		formatter: 'formatReceivedTMS'
	}, {
		field: 'sender',
		visible: false,
		formatter: 'formatSender'
	}, {
		field: 'cclist',
		visible: false,
		formatter: 'formatCCList'
	}, {
		field: 'id',
		visible: false,
		formatter: 'formatID'
	}, {
		field: 'body',
		visible: false,
		formatter: 'formatBody'
	}, {
		field: 'sadness',
		visible: false,
		formatter: 'formatSadness'
	}, {
		field: 'joy',
		visible: false,
		formatter: 'formatJoy'
	}, {
		field: 'fear',
		visible: false,
		formatter: 'formatFear'
	}, {
		field: 'disgust',
		visible: false,
		formatter: 'formatDisgust'
	}, {
		field: 'anger',
		visible: false,
		formatter: 'formatAnger'
	},
	{
		field: 'keywords',
		visible: false,
		formatter: 'formatKeywords'
	}
	],
	// Initial sort field and order
	sortName: 'sentimentScore',
	sortOrder: 'asc',
	clickToSelect: true,
	// Initialize client paging.
	pagination: true,
	pageSize: 5,
	pageList: [5, 20, 50, 100],
	paginationPreText: '<-',
	paginationNextText: '->',
	// Initialize search options.
	search: true,
	// Will display the refresh button.
	showRefresh: true,
	// Will display the column top down list.
	showColumns: true,
	// Detail format setting.
	detailView: true,
	detailFormatter: 'formatDetail'
});