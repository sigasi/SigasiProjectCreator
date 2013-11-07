library IEEE;
use IEEE.std_logic_1164.all;

entity dut is
	port(
		data_out : out std_logic_vector(7 downto 0);
		data_in  : in  std_logic_vector(7 downto 0);
		valid    : out std_logic;
		start    : in  std_logic;
		clk      : in  std_logic;
		rst      : in  std_logic
	);
end entity dut;

architecture RTL of dut is
	constant MIN_COUNT : integer := 0;
	constant MAX_COUNT : integer := 5;
	signal count       : integer range 0 to MAX_COUNT;

begin
	OUTPUT_GENERATOR : process(count, data_in) is
	begin
		if count = MAX_COUNT then
			valid    <= '1';
			data_out <= data_in;
		else
			valid    <= '0';
			data_out <=(others => '0');
		end if;
	end process OUTPUT_GENERATOR;

	COUNTER : process(clk, rst) is
	begin
		if rst = '1' then
			count <= 0;
		elsif rising_edge(clk) then
			if start = '1' then
				count <= 0;
			elsif count < MAX_COUNT then
				count <= count + 1;
			end if;
		end if;
	end process COUNTER;

end architecture RTL;
