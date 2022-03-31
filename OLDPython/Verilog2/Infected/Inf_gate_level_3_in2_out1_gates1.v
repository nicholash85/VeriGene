module Inf_gate_level_3(output out0, input in0, in1, DeletionTrigger0);
	wire faultWire0;

	xnor(faultWire0,in1,in0);  //FAULT GATE DOS EXTERNALLY TRIGGERED ON FLASE
	and(out0,faultWire0,DeletionTrigger0);   //FAULT GATE DOS EXTERNALLY TRIGGERED ON FALSE
endmodule