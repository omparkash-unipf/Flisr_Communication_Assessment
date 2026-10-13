# Switches Definition

switches = {
    "SW_MAIN_SSA": "CLOSED",
    "SW_DSA1": "CLOSED",
    "SW_DSA2": "CLOSED",
    "SW_DSA3": "CLOSED",
    "SW_TIE": "OPEN",
    "SW_MAIN_SSB": "CLOSED",
    "SW_DSB1": "CLOSED",
    "SW_DSB2": "CLOSED",
    "SW_DSB3": "CLOSED"
}

# Loads Definition
sections= {
    "Load_DSA1": {"load_MW": 1.0},
    "Load_DSA2": {"load_MW": 1.5},
    "Load_DSA3": {"load_MW": 2.0},
    "Load_DSB1": {"load_MW": 1.0},
    "Load_DSB2": {"load_MW": 1.5},
    "Load_DSB3": {"load_MW": 2.0},

}

# Network Topology
connections = {
    "SSA": "SW_MAIN_SSA",

    "SW_MAIN_SSA": "Line_DSA0",
    "Line_DSA0": "SW_DSA1",

    "SW_DSA1": "Line_DSA1",
    "Line_DSA1": "SW_DSA2",

    "SW_DSA2": "Line_DSA2",
    "Line_DSA2": "SW_DSA3",

    "SW_DSA3": "Line_DSA3",
    "Line_DSA3": "SW_TIE",

    "SW_TIE": "Line_DSB3",
    "Line_DSB3": "SW_DSB3",

    "SW_DSB3": "Line_DSB2",
    "Line_DSB2": "SW_DSB2",

    "SW_DSB2": "Line_DSB1",
    "Line_DSB1": "SW_DSB1",

    "SW_DSB1": "Line_DSB0",
    "Line_DSB0": "SW_MAIN_SSB",

    "SW_MAIN_SSB": "SSB"
}

print("\nNetwork Topology:")
print(connections)

def is_load_energized(load_name):
    
    if load_name == "Load_DSA1":
        if switches["SW_MAIN_SSA"] == "CLOSED" and switches["SW_DSA1"] == "CLOSED":
            return True
        else:
            return False
print("\nLoad Status:")
print("Load_DSA1:", is_load_energized("Load_DSA1"))