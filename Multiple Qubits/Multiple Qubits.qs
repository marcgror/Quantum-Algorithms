namespace State {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;

    // ...
open Microsoft.Quantum.Diagnostics;

operation SeparableState () : Unit {
    // allocate the qubits
    using ((q1, q2, q3) = (Qubit(), Qubit(), Qubit())) {
        // put each of the qubits q2 and q3 into superposition of 0 and 1
        H(q2);
        H(q3);
        
        // output the wave function of the three-qubit state
        DumpMachine();

        // make sure the qubits are back to the 0 state
        ResetAll([q1, q2, q3]);
    }
}
operation PrepareBellPairs () : Unit {
    // allocate the 2 qubits
    using ((a, b) = (Qubit(), Qubit())) {
        H(a); // Place qubit a into superposition
        CNOT (a, b); // Entangle
        Message ($"Measurements: {M(a)}, {M(b)}"); // Print measurements
        ResetAll([a,b]); // Reset qubits
    }
}
}