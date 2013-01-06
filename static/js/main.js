var BOARD_SIZE, click, ids, update_board;

BOARD_SIZE = 5;

ids = {};

update_board = function() {
  return $.getJSON("/game/json/state/" + id, {}, function(json) {
    var board, can_open, i, o, x, y, _i, _j, _len, _results;
    can_open = json.can_open;
    board = json.board;
    console.log("T");
    _results = [];
    for (_i = 0, _len = can_open.length; _i < _len; _i++) {
      o = can_open[_i];
      x = o.x;
      y = o.y;
      console.log("#board_" + x + "_" + y);
      if (board[y][x] !== "") {
        console.log(board[y][x]);
        for (i = _j = 1; _j <= 4; i = ++_j) {
          $("#board_" + x + "_" + y + ">div").removeClass("dir" + i);
        }
        $("#board_" + x + "_" + y + ">div").addClass(user_to_plane[board[y][x]]);
      }
      $("#board_" + x + "_" + y + ">div>.plane-front").html("<a target='_blank' href='http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=" + o.id + "&lang=jp'>" + o.id + "</a>");
      _results.push(ids[y * BOARD_SIZE + x] = "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=" + o.id + "&lang=jp");
    }
    return _results;
  });
};

$(document).ready(function() {
  update_board();
  return setInterval(function() {
    return update_board();
  }, 10000);
});

click = function(x, y) {
  alert("test");
  return document.location = ids[y * BOARD_SIZE + x];
};
