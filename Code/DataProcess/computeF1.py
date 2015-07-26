# __author__ = 'cjweffort'
# -*- coding: utf-8 -*-

def computeF1(precision, recall):
    print 'precision = %.2lf, recall = %.2lf, F1 = %.2lf' %(precision, recall, 2.0 * precision * recall / (precision + recall))

if __name__ == '__main__':
    computeF1(34.25, 0.03)
    computeF1(4.65, 0.12)
    computeF1(20.30, 0.31)
    computeF1(3.59, 0.13)
    computeF1(30.23, 0.10)
    computeF1(4.44, 0.42)
    computeF1(17.12, 0.86)
    computeF1(2.11, 0.24)
    computeF1(23.89, 0.19)
    computeF1(3.59, 0.82)
    computeF1(14.16, 1.88)
    computeF1(1.06, 0.36)
    computeF1(16.49, 0.41)
    computeF1(1.48, 0.90)
    computeF1(9.51, 3.64)
    computeF1(0.42, 0.43)