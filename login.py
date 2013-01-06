from flask import *
import functools
import hashlib
import urllib

def require_login(func):
    @functools.wraps(func)
    def wrapeer(*args, **kwargs):
        if (session.has_key("username") == True and session.has_key("passwd") == True):
            user = g.db.users.find_one({"username": session["username"], "passwd": session["passwd"]});
            if (user == None):
                return ("Invalid User");
            kwargs["user"] = user;
        else:
            path = request.path;
            get_request = urllib.urlencode({
                "redirect": path
            });
            return (redirect("/login?" + get_request));

        return func(*args, **kwargs);
    return wrapeer;

def validate_user(username):
    def _(func):
        @functools.wraps(func)
        def __(*args, **kwargs):
            if (session["username"] != username):
                return ("Invalit User");
            return func(*args, **kwargs);
        return __;
    return _;

def user_login(username, passwd):
    passwd_hash = hashlib.sha1(passwd).digest().encode("base64");

    user = g.db.users.find_one({"username": username, "passwd": passwd_hash});
    if (user):
        session["username"] = username;
        session["passwd"] = passwd_hash;
        return user
    return None

def user_logout():
    session.pop("username");
    session.pop("passwd");

def user_create(username, passwd):
    passwd_hash = hashlib.sha1(passwd).digest().encode("base64");
    new_id = g.db.users.count();
    user = g.db.users.find_one({"username": username});
    if (user == None):
        user = {"_id": new_id, "username": username, "passwd": passwd_hash}
        return (user);
    return (None);

