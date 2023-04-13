module counter #(
    parameter BITS = 32
)(
    input clk,
    input reset,
    output reg [BITS-1:0] count
);
    always @(posedge clk) begin
        if (reset) begin
            count <= 0;
        end else begin
            count <= count + 1;
        end
    end
endmodule
