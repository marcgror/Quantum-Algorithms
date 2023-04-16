# Import required packages
import streamlit as st
import plotly.graph_objects as go
import  numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ, BasicAer, transpile
from qiskit.visualization import plot_state_qsphere, plot_bloch_multivector, plot_histogram
import math
import pandas as pd
st.set_page_config(page_title='Qiskit', layout='wide')

with st.expander('Single-qubit gate selector'):
    # Use the AerSimulaor backend
    backend = Aer.get_backend('aer_simulator_statevector')
    # Define a QuantumRegister with 1 qubit                                                     
    reg = QuantumRegister(1, name='reg')
    # Define a ClassicalRegister with 1 bit
    reg_c = ClassicalRegister(1, name='regc')
    # Create a Quantum circuit with 1 qubit and 1 bit
    qc = QuantumCircuit(reg, reg_c)
    # Write the value 0
    qc.reset(reg)
    # Define the tabs
    tab1, tab2 = st.tabs(['Options', 'Figures'])
    # Define the dictionary for the gates to apply
    gates_dictionary = {'H':qc.h, 'I':qc.id, 'P':qc.p, 'RX':qc.rx, 'RY':qc.ry, 'RZ':qc.rz, 'S':qc.s, 'St':qc.sdg, 'SX':qc.sx, 'T':qc.t, 'Tt':qc.tdg, 'U':qc.u, 'X':qc.x, 'Y':qc.y, 'Z':qc.z}
    # Display a widget to select the number of gates to apply
    gates_num = tab1.number_input(label='Insert the number of gates to apply', min_value=1, value=1, step=1)
    # Display widgets to add gates to circuits
    gates_selected = []
    phase_to_apply = []
    for i in np.arange(0, gates_num, step=1):
        # Create 2 columns
        col1, col2, col3 = tab1.columns(3)
        col1.markdown(' - **Gate ' + str(i+1) + '**')
        # Display a widget to select a gate
        gate_selected = col2.selectbox(label='Select the gate to apply to qubit 0', options=gates_dictionary.keys(), key='gate' + str(i))
        # Display a widget for the phase angle to apply if required
        if gate_selected in ['P', 'RX', 'RY', 'RZ','U']:
            phi= col3.number_input('Select the phase angle rotation to apply to qubit 0', min_value=0.0, max_value=math.pi*2 + math.pi/8, step=math.pi/8, key='phase' + str(i), help='Increase/decrease by pi/8')
        else:
            phi = 0
        # Append selected gate and phase
        gates_selected.append(gate_selected)
        phase_to_apply.append(phi)
    # Apply the gate, with phase angle if correspond
    for gate in gates_selected:
        if gate in ['P', 'RX', 'RY', 'RZ','U']:
            gates_dictionary[gate](phase_to_apply[gates_selected.index(gate)], 0)
        else:
            gates_dictionary[gate](0)
    # Save the statevector
    qc.save_statevector()
    # Read the result as a digital bit
    qc.measure(reg, reg_c)
    # Transpile the circuit
    tqc = transpile(qc, backend=backend)
    job = backend.run(tqc)
    result = job.result()
    counts = result.get_counts(tqc)
    statevector = result.get_statevector()
    # Create Figures for qsphere and block
    fig_qsphere = plot_state_qsphere(statevector, figsize=(4,4))
    fig_block = plot_bloch_multivector(statevector, figsize=(1,1))
    # Display the circuit
    fig_circuit = qc.draw(output='mpl', scale=0.75)
    tab1.pyplot(fig_circuit, use_container_width=False)
    # Display the 
    tab2.pyplot(fig_qsphere, use_container_width=False)
    tab2.divider()
    # Create 2 columns
    col1, col2 = tab2.columns(2)
    col1.pyplot(fig_block, use_container_width=False)
    # Create a Figure for the bit values
    fig_hist_counts = go.Figure()
    fig_hist_counts.add_trace(go.Bar(x=list(counts.keys()), y=list(counts.values())))
    fig_hist_counts.update_xaxes(title='Bits', tickfont_size=15, titlefont=dict(size=15), )
    fig_hist_counts.update_yaxes(title='Counts', tickfont_size=15, titlefont=dict(size=15))
    col2.plotly_chart(fig_hist_counts)
