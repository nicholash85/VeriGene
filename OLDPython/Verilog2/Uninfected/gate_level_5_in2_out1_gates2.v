module gate_level_5(output out0, input in0, in1);
	wire wire0;

	and(wire0,in1,in0);
	nor(out0,wire0,in0);
endmodule