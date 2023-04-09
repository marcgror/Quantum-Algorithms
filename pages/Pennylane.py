import pennylane as qml
from pennylane import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.title('Pennylane')

with st.expander(label='Qubit rotation'):
    dev1 = qml.device("default.qubit", wires=1)

    @qml.qnode(dev1, interface='autograd')
    def circuit(params):
        qml.RX(params[0], wires=0)
        qml.RY(params[1], wires=0)
        return qml.expval(qml.PauliZ(0))

    def cost(x):
        return circuit(x)

    init_params = np.array([0.011, 0.012], requires_grad=True)

    opt = qml.GradientDescentOptimizer(stepsize=0.4)
    steps = 100
    params = init_params

    for i in range(steps):
        params = opt.step(cost, params)

        if (i + 1) % 5 ==0:
            st.markdown('Cost after step {:5d}: {:7f}'.format(i + 1, cost(params)))
    st.markdown('Optimized rotation angles:{}'.format(params))
    fig, ax = qml.draw_mpl(circuit)([np.pi/4, 0.7])
    st.pyplot(fig)