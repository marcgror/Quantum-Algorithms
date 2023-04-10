import streamlit as st
import plotly.graph_objects as go
import  numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, BasicAer, transpile
from qiskit.visualization import plot_state_qsphere, plot_bloch_multivector, plot_histogram
import math
import pandas as pd
st.set_page_config(page_title='Qiskit', layout='wide')

with st.expander('Single-qubit gate selector'):
    backend = Aer.get_backend('aer_simulator_statevector')
    reg = QuantumRegister(1, name='reg')
    reg_c = ClassicalRegister(1, name='regc')
    qc = QuantumCircuit(reg, reg_c)
    qc.reset(reg)          # write the value 0
    gates_dictionary = {'H':qc.h, 'I':qc.id, 'P':qc.p, 'RX':qc.rx, 'RY':qc.ry, 'RZ':qc.rz, 'S':qc.s, 'St':qc.sdg, 'SX':qc.sx, 'T':qc.t, 'Tt':qc.tdg, 'U':qc.u, 'X':qc.x, 'Y':qc.y, 'Z':qc.z}
    col1, col2 = st.columns(2)
    gate_selected = col1.selectbox(label='Select the gate to apply to qubit 0', options=gates_dictionary.keys())
    phi= col2.number_input('Select the phase angle rotation to apply to qubit 0', min_value=0.0, max_value=math.pi*2 + math.pi/8, step=math.pi/8)
    if gate_selected in ['P', 'RX', 'RY', 'RZ','U']:
        gates_dictionary[gate_selected](phi, 0)
    else:
        gates_dictionary[gate_selected](0)
    qc.save_statevector()
    qc.measure(reg, reg_c) # read the result as a digital bit
    tqc = transpile(qc, backend=backend)
    job = backend.run(tqc)
    result = job.result()
    counts = result.get_counts(tqc)
    statevector = result.get_statevector()
    fig_qsphere = plot_state_qsphere(statevector, figsize=(4,4))
    fig_block = plot_bloch_multivector(statevector, figsize=(2,2))
    st.pyplot(fig_qsphere, use_container_width=False)
    st.pyplot(fig_block, use_container_width=False)
    col1, col2 = st.columns(2)
    fig_circuit = qc.draw(output='mpl', scale=0.5)
    col1.pyplot(fig_circuit, use_container_width=False)
    fig_hist_counts = go.Figure()
    fig_hist_counts.add_trace(go.Bar(x=list(counts.keys()), y=list(counts.values())))
    fig_hist_counts.update_xaxes(title='Bits', tickfont_size=15, titlefont=dict(size=15), )
    fig_hist_counts.update_yaxes(title='Counts', tickfont_size=15, titlefont=dict(size=15))
    col2.plotly_chart(fig_hist_counts)
