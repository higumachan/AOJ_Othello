#coding: utf-8
from xml.etree.ElementTree import *
import random
import os
from subprocess import Popen
from flask import *

def xml2dict(xml):
    result = {};

    if (type(xml) == str):
        xml = fromstring(xml);
    if not list(xml):
        return xml.text.strip();
    for c in list(xml):
        if (result.has_key(c.tag)):
            if (type(result[c.tag]) != list):
                result[c.tag] = [result[c.tag]];
            else:
                result[c.tag].append(xml2dict(c));
        else:
            result[c.tag] = xml2dict(c);
    
    return result;

def shuffle(l):
    xi = lambda :random.randint(0, len(l) - 1);
    for i in range(500):
        a = xi();
        b = xi();
        l[a], l[b] = l[b], l[a]
    return l

def unique(seq, comp=lambda a, b: a - b, eq=lambda a, b: a == b):
    l = sorted(seq, comp);
    result = l[:1];
    for s in l[1:]:
        if (not eq(s, result[-1])):
            result.append(s);
    return result;

def start_game_command(game):
    problem_ids = " ".join(reduce(lambda x, y: x + y, game["problems_board"], []));
    command = "python game.py " + " ".join((str(game["_id"]), str(problem_ids), " ".join(game["users"])))
    process = Popen(command.split(" "));
    game["pid"] = process.pid;
    g.db.game_info.save(game);

if __name__ == "__main__":
    print xml2dict("""
<b>
<c>nadeko</c>
</b>
    """);
    print shuffle(range(200));
    print unique([3, 2, 4, 4, 5, 5, 3])
