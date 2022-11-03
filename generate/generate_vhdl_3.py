def vhdl_nqueens(n):
    with open('nqueens_3.txt', 'w') as f:
        f.write("architecture rtl of top_nqueens is \n\n")
        for i in range(n-1, 0, -1):
            f.write("    constant K_{}: integer := {}; \n".format(i,i))
            f.write("    signal a_in_{}: std_logic_vector((N*K_{}-1) downto 0); \n".format(i,i))
            f.write("    signal a_out_{}: std_logic_vector((N*(K_{}+1)-1) downto 0); \n".format(i,i))
            f.write("    signal ack_in_{}, next_in_{}, ack_out_{}, next_out_{}: std_logic; \n".format(i,i,i,i))
            f.write("    signal output_state_{}: std_logic_vector(2 downto 0); \n".format(i))
            f.write("    signal wen{}, ren{}, aful{}, emp{}: std_logic; \n".format(i,i,i,i))
            f.write("    signal din{}, dou{}: std_logic_vector((N*K_{}-1) downto 0); \n\n".format(i,i,i))    
        f.write("    signal last_candi: unsigned(N-1 downto 0); \n")
        f.write("    signal last_digit: unsigned(N-1 downto 0); \n")
        f.write("    signal counter_s: unsigned(P-1 downto 0); \n")
        f.write("    signal done_s: std_logic; \n")
        f.write("    constant impar_vector: std_logic_vector(0 downto 0) := std_logic_vector(to_unsigned(M mod 2, 1)); \n")
        f.write("    constant impar: std_logic := impar_vector(0);\n\n")        
        
        f.write("begin \n\n")
        for i in range(n-1, 0, -1):
            f.write("    fsm_{}: entity work.fsm \n".format(i))
            f.write("    generic map (K => {}, M => M, N =>N) \n".format(i))
            f.write("    port map (clk=>clk, nRst=>nRst, a_in=>a_in_{}, ack_in=>ack_in_{}, next_in=>next_in_{}, a_out=>a_out_{}, ack_out=>ack_out_{}, next_out=>next_out_{}, output_state=>output_state_{}); \n\n".format(i,i,i,i,i,i,i))
        for i in range(n-1, 0, -1): 
            f.write("    fifo_{}: entity work.fifo \n".format(i))
            f.write("    generic map(DWIDTH => N*K_{}, DEPTH => F, AFULLOFFSET => 1, AEMPTYOFFSET => 1, ASYNC => False) \n".format(i))
            f.write("    port map(wclk_i=>clk, rclk_i=>clk, wrst_i=>nRst, rrst_i=>nRst, data_i => din{}, wen_i => wen{}, ren_i => ren{}, data_o => dou{}, afull_o => aful{}, empty_o => emp{}); \n\n".format(i,i,i,i,i,i))
        for i in range(n-1, 1, -1):
            f.write("    ack_in_{} <= emp{}; \n".format(i,i))
            f.write("    a_in_{} <= dou{}; \n".format(i,i))
            f.write("    ren{} <= next_out_{}; \n".format(i,i))
            f.write("    wen{} <= not ack_out_{}; \n".format(i,i-1))
            f.write("    din{} <= a_out_{}; \n".format(i,i-1))
            f.write("    next_in_{} <= not aful{}; \n\n".format(i-1,i))
        f.write("    ack_in_1 <= emp1; \n")
        f.write("    a_in_1 <= dou1; \n")
        f.write("    ren1 <= next_out_1; \n")
        f.write("    done <= done_s; \n")
        f.write("    counter <= std_logic_vector(counter_s); \n")
        f.write("    last_digit <= unsigned(a_in_{}((N*(M-1)-1) downto (N*(M-2)))); \n".format(n-1))
        f.write("    last_candi <= (to_unsigned(M/2, N) + 1)  when impar = '1' else \n")
        f.write("                  (to_unsigned(M/2, N))      when impar = '0'; \n\n")
        for i in range(n-1, 0, -1):
            f.write("    p_a_in_{}  <= a_in_{}; \n".format(i,i))
            f.write("    p_a_out_{} <= a_out_{}; \n".format(i,i))
        f.write("    p_ack_out <= ack_out_{}; \n\n".format(n-1))    
            
        f.write("    counter_process: process(nRst, clk) \n")
        f.write("    begin \n")
        f.write("        if nRst = '1' then \n")
        f.write("            next_in_{} <= '0'; \n".format(n-1))
        f.write("            counter_s <= (others=>'0'); \n")
        f.write("        else \n")
        f.write("            next_in_{} <= '1'; \n".format(n-1))
        f.write("            if (clk'event and clk = '1') then\n")
        f.write("                if (ack_out_{} = '0' and output_state_{} = \"101\") then \n".format(n-1, n-1))
        f.write("                    if (impar = '1' and last_digit = last_candi) then \n")
        f.write("                        counter_s <= counter_s + 1; \n")
        f.write("                    else \n")
        f.write("                        counter_s <= counter_s + 2; \n")
        f.write("                    end if; \n")
        f.write("                end if; \n")
        f.write("            end if; \n")
        f.write("        end if; \n")
        f.write("    end process; \n\n")

        f.write("    init_process: process(nRst, clk) \n")
        f.write("    begin \n")
        f.write("        if nRst = '1' then \n")
        f.write("            done_s <= '0'; \n")
        f.write("            wen1 <= '0'; \n")
        f.write("            din1 <= (others=>'0'); \n")
        f.write("        elsif (clk'event and clk = '1') then \n")
        done_s = "done_s <= ("
        for i in range(1,n):
            done_s = done_s + "emp{}".format(i)
            if (i!=n-1):
                done_s = done_s + " and "
        done_s = done_s + "); \n"        
        f.write("            "+done_s)
        f.write("            if (aful1 = '0' and unsigned(din1) < last_candi) then \n")
        f.write("                din1 <= std_logic_vector(unsigned(din1) + 1); \n")
        f.write("                wen1 <= '1'; \n")
        f.write("            else \n")
        f.write("                wen1 <= '0'; \n")
        f.write("            end if; \n")
        f.write("        end if; \n")
        f.write("    end process; \n\n")
        f.write("end architecture;")

vhdl_nqueens(11)

"""
    p_a_in_10  : out std_logic_vector((N*10-1) downto 0); 
    p_a_out_10 : out std_logic_vector((N*11-1) downto 0);
    p_a_in_9   : out std_logic_vector((N*9-1) downto 0);
    p_a_out_9  : out std_logic_vector((N*10-1) downto 0);
    p_a_in_8   : out std_logic_vector((N*8-1) downto 0);
    p_a_out_8  : out std_logic_vector((N*9-1) downto 0);
    p_a_in_7   : out std_logic_vector((N*7-1) downto 0);
    p_a_out_7  : out std_logic_vector((N*8-1) downto 0);
    p_a_in_6   : out std_logic_vector((N*6-1) downto 0);
    p_a_out_6  : out std_logic_vector((N*7-1) downto 0);
    p_a_in_5   : out std_logic_vector((N*5-1) downto 0);
    p_a_out_5  : out std_logic_vector((N*6-1) downto 0);
    p_a_in_4   : out std_logic_vector((N*4-1) downto 0);
    p_a_out_4  : out std_logic_vector((N*5-1) downto 0);
    p_a_in_3   : out std_logic_vector((N*3-1) downto 0);
    p_a_out_3  : out std_logic_vector((N*4-1) downto 0);
    p_a_in_2   : out std_logic_vector((N*2-1) downto 0);
    p_a_out_2  : out std_logic_vector((N*3-1) downto 0);
    p_a_in_1   : out std_logic_vector((N*1-1) downto 0);
    p_a_out_1  : out std_logic_vector((N*2-1) downto 0);
    p_ack_out  : out std_logic;
"""