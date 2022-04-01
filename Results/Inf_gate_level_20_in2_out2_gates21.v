module Inf_gate_level_20(output out0, out1, input in0, in1);
	wire faultWire0, randOut0, wire0, wire1, wire2, wire3, wire4, wire5, wire6, wire7, wire8, wire9, wire10, wire11, wire12, wire13, wire14, wire15, wire16, wire17, wire18;

	nor(wire0,in0,in1);
	xnor(wire1,wire0,in1);
	or(wire2,in1,in0);
	nor(wire3,wire2,wire0);
	and(faultWire0,wire0,wire1);  //FAULT INTERNALLY TRIGGERED
	and(randOut0,wire2,wire0);   //FAULT INTERNALLY TRIGGERED
	xor(wire4,randOut0,faultWire0);   //FAULT INTERNALLY TRIGGERED
	xnor(wire5,wire2,wire0);
	xor(wire6,wire2,wire4);
	xnor(out0,in0,in1);
	xnor(wire7,in0,wire6);
	or(wire8,wire6,wire2);
	nand(wire9,wire6,wire1);
	xor(wire10,in0,wire7);
	nor(wire11,wire9,in1);
	xnor(wire12,wire2,wire7);
	nor(wire13,in0,wire5);
	and(wire14,wire1,wire13);
	nand(wire15,wire0,wire10);
	xnor(wire16,wire15,wire12);
	and(wire17,wire14,wire11);
	xor(wire18,wire8,wire16);
	nand(out1,wire18,wire3);
endmodule