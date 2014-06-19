#coding: utf-8

from flask import *
from logging.handlers import *
from settings import *
from login import *
import pymongo
import json
from utility import shuffle, unique, start_game_command
import datetime

app = Flask(__name__);

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
error_log = os.path.join(app.root_path, 'logs/error.log')
error_file_handler = RotatingFileHandler(
    error_log, maxBytes=100000, backupCount=10
)    
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
app.logger.addHandler(error_file_handler)

app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT";

@app.before_request
def before_request():
    g.conn = pymongo.Connection(host=DB_HOST);
    g.db = g.conn[DB_NAME];

@app.teardown_request
def teardown_request(exception):
    g.conn.close();

@app.route("/")
def index():
    return "HelloWorld"

@app.route("/game/create", methods=["GET", "POST"])
def create_game():
    if (request.method == "POST"):
        form = request.form;
        level = form["level"];
        #problems = list(g.db.problems.find({"level": level}));
        problems = list(g.db.problems.find().limit(25));
        problems = shuffle(problems)[:BOARD_SIZE ** 2];
        game = {
            "_id": g.db.game_info.count() + 1,
            "name": form["name"],
            "passwd": form["passwd"],
            "user_count": int(form["user_count"]),
            "problems_board": [["" for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)],
            "users": [],
            "is_active": False,
            "level": level,
        };
        
        for i in range(len(problems)):
            game["problems_board"][i / BOARD_SIZE][i % BOARD_SIZE] = problems[i]["id"];
        g.db.game_info.save(game);
        g.db.board_info.save({
            "_id": g.db.board_info.count() + 1,
            "game_id": game["_id"],
            "board": [["" for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)],
            "time": datetime.datetime.now(),
        });

        return redirect("/");
    else:
        return render_template("create_game.html");

@app.route("/game/list")
def game_list():
    games = g.db.game_info.find().sort("_id", -1);
    return render_template("game_list.html", games=games);

@app.route("/game/start/<int:id>")
@require_login
def start_game(id, user=None):
    game = g.db.game_info.find_one({"_id": id});
    if (game["user_count"] != len(game["users"])):
        return u"定員が足りていません";
    start_game_command(game);
    return redirect("/");

@app.route("/game/join/<int:id>")
@require_login
def join_game(id, user=None):
    game = g.db.game_info.find_one({"_id": id});
    if (game["user_count"] <= len(game["users"])):
        return render_template("/game/list", message=u"満員です");
    game["users"].append(user["username"]);

    g.db.game_info.save(game);

    return redirect("/game/buttle/%d" % id);

@app.route("/game/buttle/<int:id>")
@require_login
def buttle_game(id, user):
    game = g.db.game_info.find_one({"_id": id});
    if (not user["username"] in game["users"]):
        return "Not Entry User"
    return render_template("simple_observe.html", id=id, game=game, user=user);

@app.route("/game/observe/<int:id>")
@require_login
def observe_game(id, user):
    game = g.db.game_info.find_one({"_id": id});
    return render_template("simple_observe.html", id=id, game=game);

@app.route("/game/json/state/<int:id>")
def game_state(id):
    game = g.db.game_info.find_one({"_id": id});
    board_info = g.db.board_info.find().sort("_id", -1).limit(1)[0];
    board = board_info["board"];
    can_open = [];
    can_open.append({
        "x": 2,
        "y": 2,
        "id": game["problems_board"][2][2],
    });
    for y in range(1, BOARD_SIZE - 1):
        for x in range(1, BOARD_SIZE - 1):
            if (board[y][x] != ""):
                for d in range(-1, 2):
                    can_open.append({
                        "x": (x + d),
                        "y": (y),
                        "id": game["problems_board"][y][x + d],
                    });
                    can_open.append({
                        "x": (x),
                        "y": (y + d),
                        "id": game["problems_board"][y + d][x],
                    });
    can_open = unique(can_open, 
        lambda a, b: int(a["id"]) - int(b["id"]), lambda a, b: a["id"] == b["id"]);

    result = {
        "board": board,
        "can_open": can_open,
    };
    print json.dumps(result)
    return (json.dumps(result));
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        if (request.args.has_key("redirect") == True):
            redirect_url = request.args["redirect"];
        else:
            redirect_url = "/";
        username = request.form["username"];
        passwd = request.form["passwd"];
        user_login(username, passwd);
        return redirect(redirect_url);

    return (render_template("login.html"));

@app.route("/logout", methods=["GET", "POST"])
def logout():
    user_logout();
    return (redirect("/"));

@app.route("/create", methods=["GET", "POST"])
def regist_user():
    if (request.method == "POST"):
        username = request.form["username"];
        passwd = request.form["passwd"];
        user = user_create(username, passwd);
        if (user == None):
            return (render_template("regist.html", error=u"ユーザー名が重複しています"));
        user["is_active"] = request.form["is_active"];
        g.db.users.save(user);
        return (redirect("/login"));
    return (render_template("regist.html"));



if __name__ == "__main__":
    app.debug = True;
    app.run();

