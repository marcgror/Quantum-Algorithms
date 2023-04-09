import streamlit as st
import qsharp
from HostPython import RandomBit, RandomByte
import plotly.graph_objects as go
import  numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, BasicAer
import math
st.set_page_config(page_title='Quantum', layout='wide')

st.markdown('**Random bit**')
## Example 2-1: Random bit
# Set up the program
reg = QuantumRegister(1, name='reg')
reg_c = ClassicalRegister(1, name='regc')
qc = QuantumCircuit(reg, reg_c)

qc.reset(reg)          # write the value 0
qc.h(reg)              # put it into a superposition of 0 and 1
qc.measure(reg, reg_c) # read the result as a digital bit

backend = BasicAer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()

counts = result.get_counts(qc)
st.markdown('counts:' + str(counts))

outputstate = result.get_statevector(qc, decimals=3)
st.markdown(outputstate)
fig = qc.draw(output='mpl')        # draw the circuit
st.markdown(fig.get_size_inches())
st.pyplot (fig, use_container_width=False)
st.markdown('---')