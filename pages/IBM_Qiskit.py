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
    tab1.divider()
    fig_circuit = qc.draw(output='mpl', scale=0.75)
    tab1.markdown('**Circuit**')
    tab1.pyplot(fig_circuit, use_container_width=False)
    # Display the 
    tab2.pyplot(fig_qsphere, use_container_width=False)
    tab2.divider()
    # Create 2 columns
    col1, col2 = tab2.columns(2)
    col1.pyplot(fig_block, use_container_width=False)
    # Create a Figure for the bit values
    counts_df = pd.DataFrame()
    counts_df['keys'] = counts.keys()
    counts_df['values'] = counts.values()
    fig_hist_counts = go.Figure()
    fig_hist_counts.add_trace(go.Bar(x=list(counts_df['keys']), y=list(counts_df['values']), name='Counts', customdata=counts_df, hovertemplate='<b> Value: </b> %{customdata[0]} <br> <b>Counts: </b> %{customdata[1]}'))
    fig_hist_counts.update_xaxes(title='Bits', tickfont_size=15, titlefont=dict(size=15), dtick=1)
    fig_hist_counts.update_yaxes(title='Counts', tickfont_size=15, titlefont=dict(size=15))
    fig_hist_counts.update_layout(hoverlabel=dict(font_size=16))
    col2.plotly_chart(fig_hist_counts)
with st.expander('Multi-qubit gates selector'):
    # Define the tabs
    tab1, tab2 = st.tabs(['Options', 'Figures'])
    # Define the dictionary for the gates to apply
    col1, col2, col3, col4 = tab1.columns(4)
    qubits_num = col1.number_input('Select the number of qubits in the circuit', min_value=1, step=1)
    n_shoots  =col2.number_input('Introduce the number of shoots for the circuit', min_value=1, value=1000)
    # Use the AerSimulaor backend
    backend = Aer.get_backend('aer_simulator_statevector')
    # Define a QuantumRegister with 1 qubit                                                     
    reg = QuantumRegister(qubits_num, name='reg')
    # Define a ClassicalRegister with 1 bit
    reg_c = ClassicalRegister(qubits_num, name='regc')
    # Create a Quantum circuit with 1 qubit and 1 bit
    qc = QuantumCircuit(reg, reg_c)
    # Write the value 0
    qc.reset(reg)
    gates_dictionary_multi = {'H':qc.h, 'I':qc.id, 'P':qc.p, 'RX':qc.rx, 'RY':qc.ry, 'RZ':qc.rz, 'S':qc.s, 'St':qc.sdg, 'SX':qc.sx, 'T':qc.t, 'Tt':qc.tdg, 'U':qc.u, 'X':qc.x, 'Y':qc.y, 'Z':qc.z, 'CCX':qc.ccx, 'CH':qc.ch, 'CP':qc.cp, 'CRX':qc.crx,
        'CRY':qc.cry, 'CRZ':qc.crz, 'CSwap':qc.cswap, 'CSX':qc.csx, 'CU':qc.cu, 'CX':qc.cx, 'CY':qc.cy, 'CZ':qc.cz, 'DCX':qc.dcx, 'iSwap':qc.iswap, 'MCP':qc.mcp, 'MCX':qc.mcx, 'Swap':qc.swap}
    tab1.divider()
     # Display widgets to add gates to circuits
    for i in np.arange(0, qubits_num, step=1):
        # Create 2 columns
        col1, col2 = tab1.columns(2)
        col1.markdown(' - **Qubit ' + str(i+1) + '**')
        gates_num_multi = col2.number_input(label='Insert the number of gates to apply', min_value=1, value=1, step=1, key='gates_num_multi_' +str(i+1))
        for j in np.arange(0, gates_num_multi, step=1):
            col1, col2, col3 = tab1.columns(3)
            # Display a widget to select a gate
            gate_selected = col1.selectbox(label='Select the gate to apply to qubit ' + str(i+1), options=gates_dictionary_multi.keys(), key='gate' + str(j+1) +'_qubit' + str(i+1))
            # Display a widget for the phase angle to apply if required
            if gate_selected in ['P', 'RX', 'RY', 'RZ','U']:
                phi = col2.number_input('Select the phase angle rotation to apply to qubit ' + str(i+1), min_value=0.0, max_value=math.pi*2 + math.pi/8, step=math.pi/8, key='phase_' + str(i) + 'gate_' + str(j), help='Increase/decrease by pi/8')
                gates_dictionary_multi[gate_selected](phi, i)
            elif gate_selected in ['CP', 'CRX', 'CRY', 'CRZ', 'CU', 'MCP', 'MCX']:
                phi = col2.number_input('Select the phase angle rotation to apply to qubit ' + str(i+1), min_value=0.0, max_value=math.pi*2 + math.pi/8, step=math.pi/8, key='phase_' + str(i) + 'gate_' + str(j), help='Increase/decrease by pi/8')
                control_q = col3.multiselect('Select the control qubit(s)', options=[x for x in np.arange(1, qubits_num+1,1) if x!=(i+1)])
                gates_dictionary_multi[gate_selected](phi, [q-1 for q in control_q], i)
            # Display a widget for the control qubit(s) if required
            elif gate_selected in ['CCX', 'CH', 'CP', 'CRX', 'CRY', 'CRZ', 'CSwap', 'CSX', 'CU', 'CX', 'CY', 'CZ', 'DCX', 'iSwap', 'MCP', 'MCX', 'Swap']:
                control_q = col3.multiselect('Select the control qubit(s)', options=[x for x in np.arange(1, qubits_num+1,1) if x!=(i+1)])
                gates_dictionary_multi[gate_selected](phi, control_q, i)
            else:
                gates_dictionary_multi[gate_selected](i)
    # Save the statevector
    qc.save_statevector()
    # Read the result as a digital bit
    qc.measure(reg, reg_c)
    # Transpile the circuit
    tqc = transpile(qc, backend=backend)
    job = backend.run(tqc, shoots=n_shoots)
    result = job.result()
    counts = result.get_counts(tqc)
    statevector = result.get_statevector()
    # Create Figures for qsphere and block
    fig_qsphere = plot_state_qsphere(statevector, figsize=(4,4))
    fig_block = plot_bloch_multivector(statevector, figsize=(1,1))
    # Display the circuit
    tab1.divider()
    fig_circuit = qc.draw(output='mpl', scale=0.75)
    tab1.markdown('**Circuit**')
    tab1.pyplot(fig_circuit, use_container_width=False)
    tab1.caption(body='Figure 1: Circuit representation after applying all options')
    # Create 2 columns
    col1, col2 = tab2.columns(2)
    # Display the Q-sphere plot
    col1.markdown('**Q-sphere**')
    col1.pyplot(fig_qsphere, use_container_width=False)
    col1.caption(body='Figure 2: Q-sphere representation with all basis states')
    # Create a Figure for the counts
    counts_df = pd.DataFrame()
    counts_df['keys'] = counts.keys()
    counts_df['values'] = counts.values()
    counts_df['values'] = counts_df['values']*100/n_shoots
    # Create a Bar chart
    fig_hist_counts = go.Figure()
    fig_hist_counts.add_trace(go.Bar(x=counts_df['keys'], y=counts_df['values'], name='Counts', customdata=counts_df, hovertemplate='<b> Basis state: </b> |%{customdata[0]}> <br> <b>Probability: </b> %{customdata[1]} %'))
    # Update x-y axes
    fig_hist_counts.update_xaxes(title='Basis states', tickfont_size=15, titlefont=dict(size=15), dtick=1, type='category')
    fig_hist_counts.update_yaxes(title='Probabilities (%)', tickfont_size=15, titlefont=dict(size=15))
    # Update Figure layout
    fig_hist_counts.update_layout(height=640, hoverlabel=dict(font_size=16), xaxis={'categoryorder':'category ascending'})
    # Display the Bar chart
    col2.markdown('**Probabilities per basis state**')
    col2.plotly_chart(fig_hist_counts)
    col2.caption(body='Figure 3: Bar chart with each basis state probability')
    tab2.divider()
    # Display the Block Spheres plot
    tab2.markdown('**Block Spheres**')
    tab2.pyplot(fig_block, use_container_width=False)
    tab2.caption(body='Figure 4: Block Spheres representation for each qubit    ')
    

