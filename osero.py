#coding: utf-8

BOARD_SIZE = 5
class Osero(object):
    def __init__(self, problem_ids, size=BOARD_SIZE):
        self.board = [["" for i in range(BOARD_SIZE + 1)] for j in range(BOARD_SIZE + 1)];
        self.problem_ids = problem_ids;

    def put(self, user, pos_x, pos_y):
        self.board[pos_y][pos_x] = user;
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (not (dx == 0 and dy == 0) and self.is_reverse(user, pos_x, pos_y, dx, dy)):
                    self.reverse(user, pos_x, pos_y, dx, dy);

    def is_reverse(self, user, pos_x, pos_y, dx, dy):
        pos_x += dx;
        pos_y += dy;
        while (self.board[pos_y][pos_x] != user and self.board[pos_y][pos_x] != ""):
            pos_x += dx;
            pos_y += dy;
        return self.board[pos_y][pos_x] == user;

    def reverse(self, user, pos_x, pos_y, dx, dy):
        pos_x += dx;
        pos_y += dy;
        while (self.board[pos_y][pos_x] != user and self.board[pos_y][pos_x] != ""):
            self.board[pos_y][pos_x] = user;
            pos_x += dx;
            pos_y += dy;

    def get_position(self, problem_id):
        for i in range(len(self.problem_ids)):
            if (self.problem_ids[i] == problem_id):
                return i;

    def get_board(self):
        return map(lambda x: x[:len(x) - 1], self.board[:len(self.board) - 1]);


    def print_board(self):
        for row in self.board:
            for x in row:
                if x == "":
                    print u"□",
                else:
                    print x,;
            print 
        print 

if __name__ == "__main__":
    osero = Osero();
    osero.print_board();
    osero.put("a", 3, 3);
    osero.print_board();
    osero.put("b", 2, 2);
    osero.print_board();
    osero.put("b", 4, 4);
    osero.print_board();

