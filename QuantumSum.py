#Juan Daniel Torres 2020

from qiskit import QuantumCircuit, IBMQ ,Aer, execute
from qiskit.visualization import plot_histogram
from math import gcd, pi
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
from qiskit.quantum_info import Statevector
%matplotlib inline

#Functions for the QFT
#Taken from qiskit textbook
def qft_rotations(circuit, n):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cu1(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    """swap"""
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

def qftdag(circuit, n):
    """QFT dagger on the first n qubits in circuit"""
    swap_registers(circuit, n)
    for j in range(n):
        for m in range(j):
            circuit.cu1(-pi/float(2**(j-m)), m, j)
        circuit.h(j)
    return circuit

#We want to implement the sum operation of two numbers a and b. We do following the method described in
#ArXiv:

def getPhases(binary,N):
    """Transform a to a set of phase shitf operations in Fourier space"""
    phases = []
    
    for j in range(len(binary)):
        phases.append([])
        for i in range(len(binary)-j):
            if binary[i+j] == '1':
                phases[j].append(2**(i))
                
    return phases

def applyPhases(qr,phases):
    """Apply phase shift of a to b"""
    for i in range(len(phases)):
        for j in range(len(phases[i])):
            qr.u1(-pi/float(phases[i][j]),i)
    return qr


def Qsum(qr,abin):
    """Sum a to b"""
    return applyPhases(qr,getPhases(abin,len(abin)))


def getBitString(a,b):
    """
    This function gives proper binary string for the numbers to sum, 
    and includes an extra zero bit to avoid overflowing.
    """
    
    #Two binary string with an extra zero bit to avoid overflowing
    ab = '0'
    bb = '0'
    
    #Same bit number for a and b strings
    diff = len(format(b,'b')) - len(format(a,'b'))
    if diff>0:
        ab += diff*'0'
    else:
        bb += diff*'0'
    
    #Add binary strings at the end
    ab += format(a,'b')
    bb += format(b,'b')
    
    return [ab,bb]

def initializeQ(qr,binary):
    """This function initializes the quantum register with b"""
    for i in range(len(binary)):
        if binary[i] == '1':
            qr.x(i)
    return qr

#Sum algorithm
def sumQFT(a,b):
    """
        Sum operation of two binary numbers a and b. The steps[1] are:

        Precompute a as a phase shift:

        a) Since a is know (classical), we compute the phases added by a controled-a operations.
        b) Then we generate the set of single gate phase operations obtained in (1)

        Algorithm:

        1) Prepare a quantum register initialized to the bin rep of b
        2) Apply a QFT to the quantum register
        3) Apply the single q gates from (a) and (b)
        4) Apply QFT dagger to the quantum register

    """

    binaries = getBitString(a,b)
    N = len(binaries[0])

    qr = QuantumCircuit(N,N)
    #We do the case b=0='0...0'
    qr = initializeQ(qr,binaries[1])
    qr.barrier()
    qr = qftdag(qr,N)
    qr.barrier()
    qr = Qsum(qr,binaries[0])
    qr.barrier()
    qr = qft(qr,N)
    qr.barrier()

    for i in range(N):
        qr.measure(i,i)

    return qr


