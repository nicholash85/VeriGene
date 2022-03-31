module Inf_gate_level_5(output out0, input in0, in1, DeletionTrigger0);
	wire faultWire0, DOSNotWire0, wire0;

	and(wire0,in1,in0);
	nor(faultWire0,wire0,in0);  //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE
	not(DOSNotWire0,DeletionTrigger0); //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE 
	and(out0,faultWire0,DOSNotWire0);   //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE
endmodule