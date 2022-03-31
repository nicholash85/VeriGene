module Inf_gate_level_4(output out0, input in0, in1);
	wire faultWire0;

	nor(faultWire0,in0,in1);  //FAULT GATE DOS INTERNALLY TRIGGERED ON FALSE
	and(out0,faultWire0,in0);   //FAULT GATE DOS INTERNALLY TRIGGERED ON FALSE
endmodule