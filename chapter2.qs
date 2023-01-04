namespace HostPython {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;

    // Example 2-1: Random bit

    operation RandomBit () : Result {
        // allocate one qubit
        use q = Qubit();
        // put it into superposition of 0 and 1
        H(q);

        // measure the qubit and store the result
        let bit = M(q);
        
        // make sure the qubit is back to the 0 state
        Reset(q);
        
        return bit;
    }

    // Example 2-2: Random byte

    // open namespace which defines arithmetic operations

    operation RandomByte () : Int {
        // allocate 8 qubits
        use qs = Qubit[8];
        // put each qubit into superposition of 0 and 1
        ApplyToEach(H, qs);

        // measure the register and store the result
        // MeasureInteger returns the qubits to the |0⟩ state, so no separate Reset is required
        let randomByte = MeasureInteger(LittleEndian(qs));

        return randomByte;
    }

}