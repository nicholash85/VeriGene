module Inf_gate_level_1(output out0, input in0, in1, DeletionTrigger0);
	wire faultWire0, DOSNotWire0;

	nor(faultWire0,in0,in1);  //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE
	not(DOSNotWire0,DeletionTrigger0); //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE 
	and(out0,faultWire0,DOSNotWire0);   //FAULT GATE DOS EXTERNALLY TRIGGERED ON TRUE
endmodule