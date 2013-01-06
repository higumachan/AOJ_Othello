import functools
import pymongo
from settings import *
from flask import *

def get_db_from_id(collection_name, resname):
    a = resname;
    def _(func):
        @functools.wraps(func)
        def __(*args, **kwargs):
            id = kwargs["id"];
            result = g.db[collection_name].find_one({"_id": id});
            print collection_name, a
            if (not a):
                name = collection_name[:len(collection_name) - 1];
            kwargs[a] = result;

            return func(*args, **kwargs);
        return __;
    return _;

if __name__ == "__main__":
    app = Flask(__name__);
    app.debug = True;
    @app.before_request
    def before_request():
        g.conn = pymongo.Connection(host=DB_HOST);
        g.db = g.conn[DB_NAME];

    @app.teardown_request
    def teardown_request(exception):
        g.conn.close();

    @app.route("/<int:id>")
    @get_db_from_id("users", "user")
    def index(id, user):
        print user;
        return ("HelloWorld");

    app.run();
    
