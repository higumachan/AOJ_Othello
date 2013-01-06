#coding; utf-8

import aoj_api
import pymongo

db = pymongo.Connection().aoj_osero;

if __name__ == "__main__":
    for i in range(0, 248):
        problem = aoj_api.get_problem(i);
        problem["solved_list"] = None;
        db.problems.save(problem);

