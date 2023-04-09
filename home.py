import streamlit as st
import qsharp
from HostPython import RandomBit, RandomByte
import plotly.graph_objects as go
import  numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, BasicAer
import math
st.set_page_config(page_title='Quantum', layout='wide')

st.title('Quantum Computing')