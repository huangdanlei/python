import csv
import numpy
from numpy import *

data = open("data.csv").read()
data_r = data.split("\n")
user = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
movie = {'101': 0, '102': 1, '103': 2, '104': 3, '105': 4, '106': 5, '107': 6}
data_r = data_r[1:]
Matrix = numpy.zeros((5,7))

for row in range(len(data_r)):
	data_r[row] = data_r[row].split(",")
	x = user[str(data_r[row][0])]
	y = movie[str(data_r[row][1])]
	Matrix[x][y] = float(data_r[row][2])
    
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
	Q = Q.T
	for step in xrange(steps):
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0 :
					eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
					for k in xrange(K):
						P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
						Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
		eR = numpy.dot(P,Q)
		e = 0
		for i in xrange(len(R)):
			for j in xrange(len(R[i])):
				if R[i][j] > 0 :
					e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
					for k in xrange(K):
						e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
		if e < 0.001:
			break
	return P, Q.T

R = Matrix
R = numpy.array(R)
N = len(R)
M = len(R[0])
K = 3
P = numpy.random.rand(N,K)
Q = numpy.random.rand(M,K)
nP, nQ = matrix_factorization(R, P, Q, K)
nR = numpy.dot(nP, nQ.T)
print nR







