import pandapower as pp
from pandapower.topology import unsupplied_buses
import pandapower.shortcircuit as sc

faulted_element= None
net = pp.create_empty_network()

# Substation Buses
bus_SSA = pp.create_bus(net, vn_kv=20.0, name="SSA")
bus_SSB = pp.create_bus(net, vn_kv=20.0, name="SSB")

# External Grid at Substation A and Substation B
pp.create_ext_grid(net, bus=bus_SSA, vm_pu=1.0, s_sc_max_mva=500.0, rx_max=0.1, name="Grid_SSA")
pp.create_ext_grid(net, bus=bus_SSB, vm_pu=1.0, s_sc_max_mva=500.0, rx_max=0.1, name="Grid_SSB")

# Creating feeder buses - Substation A
bus_DSA1 = pp.create_bus(net, vn_kv=20.0, name="DSA1")
bus_DSA2 = pp.create_bus(net, vn_kv=20.0, name="DSA2")
bus_DSA3 = pp.create_bus(net, vn_kv=20.0, name="DSA3")

# Creating feeder buses - Substation B
bus_DSB1 = pp.create_bus(net, vn_kv=20.0, name="DSB1")
bus_DSB2 = pp.create_bus(net, vn_kv=20.0, name="DSB2")
bus_DSB3 = pp.create_bus(net, vn_kv=20.0, name="DSB3")

# Creating buses near tie switch
bus_TIE_A = pp.create_bus(net, vn_kv=20.0, name="TIE_A")
bus_TIE_B = pp.create_bus(net, vn_kv=20.0, name="TIE_B")


# ============================================================
# Lines - Substation A side
# ============================================================

line_DSA0 = pp.create_line_from_parameters(net, from_bus=bus_SSA, to_bus=bus_DSA1, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA0")
line_DSA1 = pp.create_line_from_parameters(net, from_bus=bus_DSA1, to_bus=bus_DSA2, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA1")
line_DSA2 = pp.create_line_from_parameters(net, from_bus=bus_DSA2, to_bus=bus_DSA3, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA2")
line_DSA3 = pp.create_line_from_parameters(net, from_bus=bus_DSA3, to_bus=bus_TIE_A, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA3")


# ============================================================
# Lines - Substation B side
# ============================================================

line_DSB0 = pp.create_line_from_parameters(net, from_bus=bus_SSB, to_bus=bus_DSB1, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB0")
line_DSB1 = pp.create_line_from_parameters(net, from_bus=bus_DSB1, to_bus=bus_DSB2, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB1")
line_DSB2 = pp.create_line_from_parameters(net, from_bus=bus_DSB2, to_bus=bus_DSB3, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB2")
line_DSB3 = pp.create_line_from_parameters(net, from_bus=bus_DSB3, to_bus=bus_TIE_B, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB3")


# ============================================================
# Switches - Substation A side
# ============================================================

pp.create_switch(net, bus=bus_SSA, element=line_DSA0, et="l", closed=True, type="L", name="SW_MAIN_SSA")
pp.create_switch(net, bus=bus_DSA1, element=line_DSA0, et="l", closed=True, type="L", name="SW_DSA1")
pp.create_switch(net, bus=bus_DSA2, element=line_DSA1, et="l", closed=True, type="L", name="SW_DSA2")
pp.create_switch(net, bus=bus_DSA3, element=line_DSA2, et="l", closed=True, type="L", name="SW_DSA3")


# ============================================================
# Switches - Substation B side
# ============================================================

pp.create_switch(net, bus=bus_SSB, element=line_DSB0, et="l", closed=True, type="L", name="SW_MAIN_SSB")
pp.create_switch(net, bus=bus_DSB1, element=line_DSB0, et="l", closed=True, type="L", name="SW_DSB1")
pp.create_switch(net, bus=bus_DSB2, element=line_DSB1, et="l", closed=True, type="L", name="SW_DSB2")
pp.create_switch(net, bus=bus_DSB3, element=line_DSB2, et="l", closed=True, type="L", name="SW_DSB3")

# Tie Switch

pp.create_switch(net, bus=bus_TIE_A, element=bus_TIE_B, et="b", closed=False, type="L", name="SW_TIE")


# ============================================================
# Loads Definition
# ============================================================

sections = {
    "Load_DSA1": {"load_MW": 1.0},
    "Load_DSA2": {"load_MW": 1.5},
    "Load_DSA3": {"load_MW": 2.0},
    "Load_DSB1": {"load_MW": 1.0},
    "Load_DSB2": {"load_MW": 1.5},
    "Load_DSB3": {"load_MW": 2.0},
}


# ============================================================
# Loads - Substation A side
# ============================================================

pp.create_load(net, bus=bus_DSA1, p_mw=sections["Load_DSA1"]["load_MW"], q_mvar=0.0, name="Load_DSA1")
pp.create_load(net, bus=bus_DSA2, p_mw=sections["Load_DSA2"]["load_MW"], q_mvar=0.0, name="Load_DSA2")
pp.create_load(net, bus=bus_DSA3, p_mw=sections["Load_DSA3"]["load_MW"], q_mvar=0.0, name="Load_DSA3")


# ============================================================
# Loads - Substation B side
# ============================================================

pp.create_load(net, bus=bus_DSB1, p_mw=sections["Load_DSB1"]["load_MW"], q_mvar=0.0, name="Load_DSB1")
pp.create_load(net, bus=bus_DSB2, p_mw=sections["Load_DSB2"]["load_MW"], q_mvar=0.0, name="Load_DSB2")
pp.create_load(net, bus=bus_DSB3, p_mw=sections["Load_DSB3"]["load_MW"], q_mvar=0.0, name="Load_DSB3")


# Here the function is created which helps to detect the fault based on electrical measurements
def detect_overcurrent(net, fault_current_threshold_ka=0.5):
    detected_lines = []

    for index, line in net.line.iterrows():
        if not line["in_service"]:
            continue

        current_ka = net.res_line.at[index, "i_ka"]

        if current_ka >= fault_current_threshold_ka:
            detected_lines.append(line["name"])
            print(f"Overcurrent detected on {line['name']}: {current_ka:.3f} kA")

    if not detected_lines:
        print("No overcurrent detected.")

    return detected_lines


def detect_short_circuit(fault_current_ka, threshold_ka=1.0):
    print("\nFault Detection:")

    if fault_current_ka >= threshold_ka:
        print(f"FAULT DETECTED: {fault_current_ka:.3f} kA")
        return True
    else:
        print(f"No fault detected: {fault_current_ka:.3f} kA")
        return False

print("\nShort-Circuit Calculation:")

sc.calc_sc(net, bus=bus_DSA3, fault="3ph", case="max")

fault_current_ka = net.res_bus_sc.at[bus_DSA3, "ikss_ka"]

print(f"Fault location: DSA3")
print(f"Initial short-circuit current: {fault_current_ka:.3f} kA")
fault_detected = detect_short_circuit(fault_current_ka)


# ------------------------------------------------------------
# Fault Location and Isolation
fault_isolation_map = {
    "Line_DSA0": "SW_DSA1",
    "Line_DSA1": "SW_DSA2",
    "Line_DSA2": "SW_DSA3",
    "Line_DSB0": "SW_DSB1",
    "Line_DSB1": "SW_DSB2",
    "Line_DSB2": "SW_DSB3"
}

faulted_element = "Line_DSA2"  # This i am hardcoding myself. based on the faulted element, the switch will be chosen automatically.

if faulted_element not in fault_isolation_map:
    raise ValueError(f"No isolation switch defined for faulted element: {faulted_element}")

isolation_switch = fault_isolation_map[faulted_element]

if not (net.line["name"] == faulted_element).any():
    raise ValueError(f"Faulted line does not exist in the network: {faulted_element}")

print(f"Fault input validated: {faulted_element}")
print(f"Assigned isolation switch: {isolation_switch}")

print("\nFault Isolation:")
print(f"Faulted element: {faulted_element}")
print(f"Isolation switch: {isolation_switch}")

# Open the fault isolation switch
isolation_switch_idx = net.switch.index[net.switch["name"] == isolation_switch][0]
net.switch.at[isolation_switch_idx, "closed"] = False

# Open the main switch at Substation A
main_switch_idx = net.switch.index[net.switch["name"] == "SW_MAIN_SSA"][0]
net.switch.at[main_switch_idx, "closed"] = False

print("SW_MAIN_SSA: OPEN")

# ============================================================
# Service Restoration
# ============================================================

print("\nService Restoration:")

# Close the main switch at Substation A
main_switch_idx = net.switch.index[net.switch["name"] == "SW_MAIN_SSA"][0]
net.switch.at[main_switch_idx, "closed"] = True

# Close the tie switch
tie_switch_idx = net.switch.index[net.switch["name"] == "SW_TIE"][0]
net.switch.at[tie_switch_idx, "closed"] = True

# Keep the fault isolation switch open
isolation_switch_idx = net.switch.index[net.switch["name"] == isolation_switch][0]
net.switch.at[isolation_switch_idx, "closed"] = False

pp.runpp(net)
detected_lines = detect_overcurrent(net)

'''
print("SW_MAIN_SSA: CLOSED")
print("SW_TIE: CLOSED")
print(f"{isolation_switch}: OPEN")
print("\nBus Voltage:")
for index, bus in net.bus.iterrows():
    voltage_pu = net.res_bus.at[index, "vm_pu"]
    voltage_kv = voltage_pu * bus["vn_kv"]
    print(f'{bus["name"]}: {voltage_kv:.3f} kV | {voltage_pu:.3f} pu')

print("\nLine Current and Loading:")
for index, line in net.line.iterrows():
    current_ka = net.res_line.at[index, "i_ka"]
    loading_percent = net.res_line.at[index, "loading_percent"]
    print(f'{line["name"]}: {current_ka:.3f} kA | Loading: {loading_percent:.2f} %')


'''
'''

# Energized and Un-Energized Loads
unsupplied = unsupplied_buses(net)

print("\nUnsupplied Bus Names:")

for bus in unsupplied:
    print(net.bus.at[bus, "name"])

# If the loads are getting energy or are the open circuit
print("\nLoad Status:")

for index, load in net.load.iterrows():
    if load["bus"] in unsupplied:
        print(f'{load["name"]}: DE-ENERGIZED')
    else:
        print(f'{load["name"]}: ENERGIZED')
'''
