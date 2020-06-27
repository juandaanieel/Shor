# Shor's Algorithm
Qiskit implementation of the Shor's algorithm based on: 

In this code we want to implement a general Shor's algorithm that does not depend on the input numbers. To do so we follow [1]. It describes a method for implement the Quantum Phase Estimation procedure with 2n+3 qubits. We will be mainly focused in the fouth step of the Shor's algorithm[1,2] since the other steps can be done in a classical computer.

This is an ongoing project.

## Quantum Sum

A circuit to sum two numbers a and b can be found in `QuantumSum.py`. We import the function `sumQFT(a,b)` that sums a number (a) to a qubit state (b). Then, we implement the sum of 3 and 2 with the following code:

```python
qr=sumQFT(3,2)
backend = BasicAer.get_backend('qasm_simulator')
job = execute(qr, backend)
plot_histogram(job.result().get_counts(), color='midnightblue', title="3(011)+2(010)=5(101)")
```
The results are:
![alt text](https://github.com/juandaanieel/Shor/blob/master/3plus2.png)
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
