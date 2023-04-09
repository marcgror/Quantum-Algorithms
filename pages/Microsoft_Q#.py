import streamlit as st
import qsharp
from HostPython import RandomBit, RandomByte
import plotly.graph_objects as go
import  numpy as np
import math
st.set_page_config(page_title='Quantum', layout='wide')

st.markdown('**Random bit**')
number_of_bites = st.number_input('Type the number of bites to simulate', min_value=1, value=30)
bits  = []
for i in np.arange(number_of_bites):
    bits.append(str(RandomBit.simulate()))
fig_bits = go.Figure()
fig_bits.add_trace(go.Histogram(x=bits, histnorm='percent'))
fig_bits.update_xaxes(title='Bit', tickfont_size=15)
fig_bits.update_yaxes(title='Probability (%)', tickfont_size=15)
fig_bits.update_layout(title='Probabilities for random bit generation')
st.plotly_chart(fig_bits)
with st.expander('Display Q# code'):
    st.code('''operation CreateQuantumRNG() : Result {
        use q = Qubit(); // Allocate a qubit.
        H(q); // Put the qubit to superposition. A Z-basis measurement now has a 50% chance of returning 0 or 1.
        return MResetZ(q); // Measure the qubit value.
    }''')
st.markdown('---')
st.markdown('**Random Byte**')
number_of_bytes = st.number_input('Input the number of bytes to simulate', min_value=1, value=30)
bytes = []
for i in np.arange(300):
    bytes.append(str(RandomByte.simulate()))
fig_bytes = go.Figure()
fig_bytes.add_trace(go.Histogram(x=bytes, histnorm='percent'))
fig_bytes.update_xaxes(title='Byte', tickfont_size=15)
fig_bytes.update_yaxes(title='Probability (%)', tickfont_size=15)
fig_bytes.update_layout(title='Probabilities for random bites generation')
st.plotly_chart(fig_bytes)
with st.expander('Display Q# code'):
    st.code('''operation RandomByte () : Unit {
    // allocate 8 qubits
    use qs = Qubit[8];
    // put each qubit into superposition of 0 and 1
    ApplyToEach(H, qs);

    // measure the register and store the result
    // MeasureInteger returns the qubits to the |0⟩ state, so no separate Reset is required
    let randomByte = MeasureInteger(LittleEndian(qs));

    Message($"{randomByte}");
    }''')
st.markdown('---')