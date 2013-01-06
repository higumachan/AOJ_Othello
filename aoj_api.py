#coding; utf-8

import urllib
import utility

def get_problem(id, status=None):
    url = "http://judge.u-aizu.ac.jp/onlinejudge/webservice/problem";
    pram = {"id": "%04d" % id};
    if (status):
        pram["status"] = status;
    pram_str = urllib.urlencode(pram);
    print pram_str

    return (utility.xml2dict(urllib.urlopen(url + "?" + pram_str).read()));

def get_solved_record(**kwargs):
    url = "http://judge.u-aizu.ac.jp/onlinejudge/webservice/solved_record";
    pram = kwargs;
    pram_str = urllib.urlencode(pram);
    
    return (utility.xml2dict(urllib.urlopen(url + "?" + pram_str).read()));

def get_status_log(**kwargs):
    url = "http://judge.u-aizu.ac.jp/onlinejudge/webservice/status_log";
    pram = kwargs;
    pram["problem_id"] = "%04d" % pram["problem_id"];
    pram_str = urllib.urlencode(pram);
    
    return (utility.xml2dict(urllib.urlopen(url + "?" + pram_str).read()));


if __name__ == "__main__":
    print get_solved_record(user_id="harekumo");
    print get_status_log(problem_id=0);

