import pandapower as pp
from pandapower.topology import unsupplied_buses
import pandapower.shortcircuit as sc


# ============================================================
# 1. CONTROLLED FAULT EVENT SETTINGS
# ============================================================

# Controlled test scenario: a three-phase fault is assumed on Line_DSA2,
# at its DSA3 end. The short-circuit calculation is performed at bus DSA3.
faulted_element = "Line_DSA2"
fault_bus_name = "DSA3"

# These values represent a simple event scheduler for this static model.
# They do NOT create a continuous-time electromagnetic simulation.
simulation_time_s = 1.0
fault_time_s = 1.0

fault_current_threshold_ka = 1.0  # Illustrative threshold; not a protection setting
short_circuit_case = "max"


# ============================================================
# 2. NETWORK CREATION
# ============================================================

net = pp.create_empty_network()

# Substation buses
bus_SSA = pp.create_bus(net, vn_kv=20.0, name="SSA")
bus_SSB = pp.create_bus(net, vn_kv=20.0, name="SSB")

# External grids: short-circuit parameters are illustrative assumptions.
pp.create_ext_grid(net, bus=bus_SSA, vm_pu=1.0, s_sc_max_mva=500.0, rx_max=0.1, name="Grid_SSA")
pp.create_ext_grid(net, bus=bus_SSB, vm_pu=1.0, s_sc_max_mva=500.0, rx_max=0.1, name="Grid_SSB")

# Feeder buses - Substation A
bus_DSA1 = pp.create_bus(net, vn_kv=20.0, name="DSA1")
bus_DSA2 = pp.create_bus(net, vn_kv=20.0, name="DSA2")
bus_DSA3 = pp.create_bus(net, vn_kv=20.0, name="DSA3")

# Feeder buses - Substation B
bus_DSB1 = pp.create_bus(net, vn_kv=20.0, name="DSB1")
bus_DSB2 = pp.create_bus(net, vn_kv=20.0, name="DSB2")
bus_DSB3 = pp.create_bus(net, vn_kv=20.0, name="DSB3")

# Buses near tie switch
bus_TIE_A = pp.create_bus(net, vn_kv=20.0, name="TIE_A")
bus_TIE_B = pp.create_bus(net, vn_kv=20.0, name="TIE_B")


# ============================================================
# 3. LINES - SUBSTATION A SIDE
# ============================================================

line_DSA0 = pp.create_line_from_parameters(net, from_bus=bus_SSA, to_bus=bus_DSA1, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA0")
line_DSA1 = pp.create_line_from_parameters(net, from_bus=bus_DSA1, to_bus=bus_DSA2, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA1")
line_DSA2 = pp.create_line_from_parameters(net, from_bus=bus_DSA2, to_bus=bus_DSA3, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA2")
line_DSA3 = pp.create_line_from_parameters(net, from_bus=bus_DSA3, to_bus=bus_TIE_A, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSA3")


# ============================================================
# 4. LINES - SUBSTATION B SIDE
# ============================================================

line_DSB0 = pp.create_line_from_parameters(net, from_bus=bus_SSB, to_bus=bus_DSB1, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB0")
line_DSB1 = pp.create_line_from_parameters(net, from_bus=bus_DSB1, to_bus=bus_DSB2, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB1")
line_DSB2 = pp.create_line_from_parameters(net, from_bus=bus_DSB2, to_bus=bus_DSB3, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB2")
line_DSB3 = pp.create_line_from_parameters(net, from_bus=bus_DSB3, to_bus=bus_TIE_B, length_km=1.0, r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4, name="Line_DSB3")


# ============================================================
# 5. SWITCHES
# ============================================================

# Substation A
pp.create_switch(net, bus=bus_SSA, element=line_DSA0, et="l", closed=True, type="L", name="SW_MAIN_SSA")
pp.create_switch(net, bus=bus_DSA1, element=line_DSA0, et="l", closed=True, type="L", name="SW_DSA1")
pp.create_switch(net, bus=bus_DSA2, element=line_DSA1, et="l", closed=True, type="L", name="SW_DSA2")
pp.create_switch(net, bus=bus_DSA3, element=line_DSA2, et="l", closed=True, type="L", name="SW_DSA3")

# Substation B
pp.create_switch(net, bus=bus_SSB, element=line_DSB0, et="l", closed=True, type="L", name="SW_MAIN_SSB")
pp.create_switch(net, bus=bus_DSB1, element=line_DSB0, et="l", closed=True, type="L", name="SW_DSB1")
pp.create_switch(net, bus=bus_DSB2, element=line_DSB1, et="l", closed=True, type="L", name="SW_DSB2")
pp.create_switch(net, bus=bus_DSB3, element=line_DSB2, et="l", closed=True, type="L", name="SW_DSB3")

# Normally-open tie switch
pp.create_switch(net, bus=bus_TIE_A, element=bus_TIE_B, et="b", closed=False, type="L", name="SW_TIE")


# ============================================================
# 6. LOADS
# ============================================================

sections = {
    "Load_DSA1": {"load_MW": 1.0},
    "Load_DSA2": {"load_MW": 1.5},
    "Load_DSA3": {"load_MW": 2.0},
    "Load_DSB1": {"load_MW": 1.0},
    "Load_DSB2": {"load_MW": 1.5},
    "Load_DSB3": {"load_MW": 2.0},
}

pp.create_load(net, bus=bus_DSA1, p_mw=sections["Load_DSA1"]["load_MW"], q_mvar=0.0, name="Load_DSA1")
pp.create_load(net, bus=bus_DSA2, p_mw=sections["Load_DSA2"]["load_MW"], q_mvar=0.0, name="Load_DSA2")
pp.create_load(net, bus=bus_DSA3, p_mw=sections["Load_DSA3"]["load_MW"], q_mvar=0.0, name="Load_DSA3")
pp.create_load(net, bus=bus_DSB1, p_mw=sections["Load_DSB1"]["load_MW"], q_mvar=0.0, name="Load_DSB1")
pp.create_load(net, bus=bus_DSB2, p_mw=sections["Load_DSB2"]["load_MW"], q_mvar=0.0, name="Load_DSB2")
pp.create_load(net, bus=bus_DSB3, p_mw=sections["Load_DSB3"]["load_MW"], q_mvar=0.0, name="Load_DSB3")


# ============================================================
# 7. HELPER FUNCTIONS
# ============================================================

def detect_short_circuit(fault_current_ka, threshold_ka=1.0):
    """Preliminary detection logic based on a calculated prospective fault current."""
    print("\nFault Detection:")
    if fault_current_ka >= threshold_ka:
        print(f"FAULT DETECTED: {fault_current_ka:.3f} kA >= {threshold_ka:.3f} kA")
        return True

    print(f"No fault detected: {fault_current_ka:.3f} kA < {threshold_ka:.3f} kA")
    return False


def print_switch_status(net):
    print("\nSwitch Status:")
    for _, switch in net.switch.iterrows():
        status = "CLOSED" if bool(switch["closed"]) else "OPEN"
        print(f'{switch["name"]}: {status}')


def print_electrical_measurements(net):
    print("\nBus Voltage:")
    for index, bus in net.bus.iterrows():
        if index in net.res_bus.index and net.res_bus.at[index, "vm_pu"] == net.res_bus.at[index, "vm_pu"]:
            voltage_pu = net.res_bus.at[index, "vm_pu"]
            voltage_kv = voltage_pu * bus["vn_kv"]
            print(f'{bus["name"]}: {voltage_kv:.3f} kV | {voltage_pu:.3f} pu')
        else:
            print(f'{bus["name"]}: voltage unavailable')

    print("\nLine Current and Loading:")
    for index, line in net.line.iterrows():
        if index in net.res_line.index:
            current_ka = net.res_line.at[index, "i_ka"]
            loading_percent = net.res_line.at[index, "loading_percent"]
            if current_ka == current_ka and loading_percent == loading_percent:
                print(f'{line["name"]}: {current_ka:.3f} kA | Loading: {loading_percent:.2f} %')
            else:
                print(f'{line["name"]}: results unavailable')


def print_load_status(net):
    unsupplied = unsupplied_buses(net)

    print("\nUnsupplied Bus Names:")
    if len(unsupplied) == 0:
        print("None")
    else:
        for bus in unsupplied:
            print(net.bus.at[bus, "name"])

    print("\nLoad Status:")
    for _, load in net.load.iterrows():
        if load["bus"] in unsupplied:
            print(f'{load["name"]}: DE-ENERGIZED')
        else:
            print(f'{load["name"]}: ENERGIZED')


# ============================================================
# 8. FAULT-TO-ISOLATION SWITCH MAP
# ============================================================

fault_isolation_map = {
    "Line_DSA0": "SW_DSA1",
    "Line_DSA1": "SW_DSA2",
    "Line_DSA2": "SW_DSA3",
    "Line_DSB0": "SW_DSB1",
    "Line_DSB1": "SW_DSB2",
    "Line_DSB2": "SW_DSB3",
}

if faulted_element not in fault_isolation_map:
    raise ValueError(f"No isolation switch defined for faulted element: {faulted_element}")

if not (net.line["name"] == faulted_element).any():
    raise ValueError(f"Faulted line does not exist in the network: {faulted_element}")

if not (net.bus["name"] == fault_bus_name).any():
    raise ValueError(f"Fault bus does not exist in the network: {fault_bus_name}")

isolation_switch = fault_isolation_map[faulted_element]
fault_bus = net.bus.index[net.bus["name"] == fault_bus_name][0]

print("Controlled FLISR scenario")
print(f"Configured faulted line: {faulted_element}")
print(f"Configured fault bus: {fault_bus_name}")
print(f"Assigned isolation switch: {isolation_switch}")
print(f"Configured fault time: {fault_time_s:.2f} s")


# ============================================================
# 9. NORMAL OPERATION BEFORE THE CONTROLLED EVENT
# ============================================================

pp.runpp(net)

print("\n=== NORMAL OPERATION ===")
print_switch_status(net)
print_electrical_measurements(net)
print_load_status(net)


# ============================================================
# 10. CONTROLLED FAULT EVENT AND SHORT-CIRCUIT STUDY
# ============================================================

fault_detected = False

if simulation_time_s >= fault_time_s:
    print(f"\n=== CONTROLLED FAULT EVENT AT t = {simulation_time_s:.2f} s ===")
    print(f"Assumed three-phase fault on {faulted_element}, at bus {fault_bus_name}")

    # This calculates the prospective three-phase short-circuit current at the
    # selected bus. It does not insert a physical fault into the load-flow model.
    sc.calc_sc(net, bus=fault_bus, fault="3ph", case=short_circuit_case)
    fault_current_ka = net.res_bus_sc.at[fault_bus, "ikss_ka"]

    print(f"Initial symmetrical short-circuit current: {fault_current_ka:.3f} kA")

    fault_detected = detect_short_circuit(fault_current_ka, threshold_ka=fault_current_threshold_ka)
else:
    print(f"\nNo fault event yet: simulation time {simulation_time_s:.2f} s is before fault time {fault_time_s:.2f} s.")


# ============================================================
# 11. CONDITIONAL FLISR: ISOLATION AND RESTORATION
# ============================================================

if fault_detected:
    print("\n=== FLISR ACTIVATED ===")

    isolation_switch_idx = net.switch.index[net.switch["name"] == isolation_switch][0]
    main_switch_idx = net.switch.index[net.switch["name"] == "SW_MAIN_SSA"][0]
    tie_switch_idx = net.switch.index[net.switch["name"] == "SW_TIE"][0]

    # Fault isolation
    print("\nFault Isolation:")
    print(f"Faulted element: {faulted_element}")
    print(f"Opening isolation switch: {isolation_switch}")
    net.switch.at[isolation_switch_idx, "closed"] = False

    # Preserve the requested operating sequence: open A main, then reclose it
    # after the faulted section has been isolated.
    net.switch.at[main_switch_idx, "closed"] = False
    print("SW_MAIN_SSA: OPEN")

    # Re-energize the healthy A-side sections and restore the isolated DSA3
    # section from Substation B through the normally-open tie.
    print("\nService Restoration:")
    net.switch.at[main_switch_idx, "closed"] = True
    net.switch.at[tie_switch_idx, "closed"] = True

    # Ensure the fault isolation switch remains open.
    net.switch.at[isolation_switch_idx, "closed"] = False

    print("SW_MAIN_SSA: CLOSED")
    print("SW_TIE: CLOSED")
    print(f"{isolation_switch}: OPEN")

    # Recalculate post-restoration power flow
    pp.runpp(net)

    print("\n=== POST-RESTORATION RESULTS ===")
    print_switch_status(net)
    print_electrical_measurements(net)

    print("\nPost-Restoration Overcurrent Check:")
    # This checks normal load-flow current after restoration, not fault current.
    post_restoration_overcurrent = []
    for index, line in net.line.iterrows():
        if not line["in_service"]:
            continue
        current_ka = net.res_line.at[index, "i_ka"]
        if current_ka >= 0.5:
            post_restoration_overcurrent.append(line["name"])
            print(f'Overcurrent threshold exceeded on {line["name"]}: {current_ka:.3f} kA')

    if not post_restoration_overcurrent:
        print("No overcurrent detected.")

    print_load_status(net)

else:
    print("\nFLISR NOT ACTIVATED: fault detection threshold was not met.")
    print("No isolation or restoration switch operations were performed.")
