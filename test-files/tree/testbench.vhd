library IEEE;
use IEEE.std_logic_1164.all;

-- Test bench for Sigasi Tutorial Project.
entity testbench is
end entity testbench;

architecture STR of testbench is
	signal data_out : std_logic_vector(7 downto 0);
	signal data_in  : std_logic_vector(7 downto 0);
	signal valid    : std_logic;
	signal start    : std_logic;
	signal clk      : std_logic;
	signal rst      : std_logic;
	constant PERIOD : time := 50 ns;    -- Half the clock period. The frequency will be 1/PERIOD = 20 MHz

begin
	clock_generator_instance : entity work.clock_generator(BEH)
		generic map(
			PERIOD => PERIOD
		)
		port map(
			clk => clk
		);

	dut_instance : entity work.dut(RTL)
		port map(
			data_out => data_out,
			data_in  => data_in,
			valid    => valid,
			start    => start,
			clk      => clk,
			rst      => rst
		);

end architecture STR;
