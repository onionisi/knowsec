import unittest
from collections import namedtuple


Op_attr = namedtuple('Op_attr', 'prec assoc')
L, R = 'L R'.split()
NUM, LPAREN, RPAREN = 'N ( )'.split()

ops = {
    '^': Op_attr(prec=4, assoc=R),
    '*': Op_attr(prec=3, assoc=L),
    '%': Op_attr(prec=3, assoc=L),
    '/': Op_attr(prec=3, assoc=L),
    '+': Op_attr(prec=2, assoc=L),
    '-': Op_attr(prec=2, assoc=L),
    '(': Op_attr(prec=9, assoc=L),
    ')': Op_attr(prec=0, assoc=L),
}


def getin(exp=None):
    if exp is None:
        exp = input('expression: ')
    tokens = exp.strip().split()
    inpvals = []
    for token in tokens:
        if token in ops:
            inpvals.append((token, ops[token]))
        else:
            inpvals.append((NUM, token))
    return inpvals


def shunt(infix):
    postfix, stack = [], []
    for token, val in infix:
        if token is NUM:
            postfix.append(val)
        elif token in ops:
            t1, (p1, a1) = token, val
            while stack:
                t2, (p2, a2) = stack[-1]
                if (a1 == L and p1 <= p2) or (a1 == R and p1 < p2):
                    if t1 != RPAREN:
                        if t2 != LPAREN:
                            stack.pop()
                            postfix.append(t2)
                        else:
                            break
                    else:
                        if t2 != LPAREN:
                            stack.pop()
                            postfix.append(t2)
                        else:
                            stack.pop()
                            break
                else:
                    break
            if t1 != RPAREN:
                stack.append((token, val))
    while stack:
        t2, (p2, a2) = stack[-1]
        stack.pop()
        postfix.append(t2)
    return ' '.join(postfix)


class DemoTests(unittest.TestCase):

    def tearDown(self):
        pass

    def test_simple(self):
        t1 = '4 + 5'
        pt1 = '4 5 +'
        t2 = '4 * 5'
        pt2 = '4 5 *'
        t3 = '4 / 5'
        pt3 = '4 5 /'
        t4 = '4 - 5'
        pt4 = '4 5 -'

        self.assertEqual(shunt(getin(t1)), pt1)
        self.assertEqual(shunt(getin(t2)), pt2)
        self.assertEqual(shunt(getin(t3)), pt3)
        self.assertEqual(shunt(getin(t4)), pt4)

    def test_parent(self):
        t1 = '4 + ( 5 - 1 )'
        pt1 = '4 5 1 - +'
        t2 = '4 ^ ( 5 + 3 )'
        pt2 = '4 5 3 + ^'
        t3 = '4 / ( 5 % 9 )'
        pt3 = '4 5 9 % /'
        t4 = '4 - ( 5 + 1 )'
        pt4 = '4 5 1 + -'

        self.assertEqual(shunt(getin(t1)), pt1)
        self.assertEqual(shunt(getin(t2)), pt2)
        self.assertEqual(shunt(getin(t3)), pt3)
        self.assertEqual(shunt(getin(t4)), pt4)

    def test_dparent(self):
        t1 = '4 + ( 6  / ( 5 - 1 ) )'
        pt1 = '4 6 5 1 - / +'

        self.assertEqual(shunt(getin(t1)), pt1)


if __name__ == "__main__":
    unittest.main()
