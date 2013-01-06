#coding: utf-8

from threading import Thread, Lock
from aoj_api import get_solved_record, get_status_log
import sys
import datetime
import pymongo
import time
from osero import Osero
from settings import *

lock = Lock();

BOARD_SIZE = 5
osero = None;

db = pymongo.Connection()[DB_NAME];

def check_problem(game_id, problem_id, users, start_time):
    while True:
        solved = get_status_log(problem_id=problem_id)["status"];
        solved = filter(lambda x: x["user_id"] in users and x["status"] == "Accepted" and int(x["submission_date"]) >= start_time, solved);
        if (solved):
            solved.sort(lambda x, y: int(x["run_id"]) - int(y["run_id"]));
            lock.acquire();
            solved_problem(problem_id, solved[0]["user_id"]);
            update_board(game_id);
            lock.release();
            break;
        #print "problem_id %d:" % problem_id, solved
        time.sleep(10);

def solved_problem(problem_id, user_id):
    index = osero.get_position(problem_id);
    osero.put(user_id, index % BOARD_SIZE, index / BOARD_SIZE);

def update_board(game_id):
    board_info = {
        "_id": db.board_info.count() + 1,
        "game_id": game_id,
        "board": osero.get_board(),
        "time": datetime.datetime.now(),
    };
    db.board_info.save(board_info);

if __name__ == "__main__":
    if (len(sys.argv) != 1):
        game_id = int(sys.argv[1]);
        problem_ids = map(int, sys.argv[2:27]);
        users = sys.argv[27: 31];
    else:
        game_id = 1;
        problem_ids = map(lambda x: "%04d" % x,  range(0, 26));
        users = ["harekumo", "rikka", "nadeko2", "nadeko3"];
    start_time = int(time.mktime(datetime.datetime.now().timetuple())) * 1000;
    osero = Osero(problem_ids);
    for problem_id in problem_ids:
        thread = Thread(target=check_problem, args=(game_id, problem_id, users, start_time));
        thread.start();
    while True:
        osero.print_board();
        time.sleep(10);

