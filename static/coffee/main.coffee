
BOARD_SIZE = 5
ids = {};
update_board = ->
	$.getJSON("/game/json/state/" + id, {}, (json)->
		can_open = json.can_open;
		board = json.board;
		console.log("T");
		for o in can_open
			x = o.x;
			y = o.y;
			console.log("#board_#{x}_#{y}");
			if board[y][x] != ""
				console.log(board[y][x]);
				$("#board_#{x}_#{y}").text(board[y][x]);
			else
				$("#board_#{x}_#{y}").html("<a target='_blank' href='http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=#{o.id}&lang=jp'>#{o.id}</a>");
			ids[y * BOARD_SIZE + x] = "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=#{o.id}&lang=jp"
	);

$(document).ready( ->
	update_board();
	setInterval(->
		update_board()
	, 10000);
)

click = (x, y) -> 
	alert("test")
	document.location = ids[y * BOARD_SIZE + x];
