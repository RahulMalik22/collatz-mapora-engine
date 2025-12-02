"""
Project: Collatz Mapora Engine (Recursive Residue Network Analyzer)
Author: Independent Researcher
Date: December 2025
Description: 
    A computational framework for analyzing the "Branching Density" of the 
    Collatz graph over finite modular fields. This engine models residue 
    classes as directed acyclic graphs to quantify structural stability.
"""

import collections
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

# ==========================================
# PART 1: THE CORE ENGINE
# ==========================================

class MaporaStack:
    """
    Represents a Residue Class defined by (modulus * k + residue).
    Tracks the logical path of the entire class through the Collatz map.
    """
    def __init__(self, modulus, residue, symbol_id, layer=0):
        self.m = modulus
        self.r = residue
        self.id = symbol_id
        self.layer = layer

    def get_next_state(self):
        """
        Determines the next logical state of the residue class.
        Returns a new MaporaStack if deterministic (Merge), or None if ambiguous (Split).
        """
        # If Residue is Even
        if self.r % 2 == 0:
            # If Modulus is Even, we can divide the whole stack cleanly.
            if self.m % 2 == 0:
                return MaporaStack(self.m // 2, self.r // 2, f"{self.id}D", self.layer + 1)
            # If Modulus is Odd, parity is ambiguous -> BIFURCATION.
            else: 
                return None

        # If Residue is Odd, we apply 3n+1.
        # This is always deterministic because 3(odd) + 1 is even, 
        # but we track the transition to the 3n+1 state.
        return MaporaStack(3 * self.m, 3 * self.r + 1, f"{self.id}M", self.layer + 1)

def get_stability_ratio(modulus, residue, depth_limit):
    """
    Calculates the Stability Ratio (Merges / Splits) for a given residue class.
    """
    queue = collections.deque([MaporaStack(modulus, residue, "ROOT")])
    straight_paths = 0
    splits = 0
    nodes = 0
    
    while queue and nodes < depth_limit:
        curr = queue.popleft()
        
        # Termination check (4-2-1 loop entry)
        if curr.r == 1 and curr.m % 2 == 0: 
            nodes += 1
            continue

        nxt = curr.get_next_state()
        
        if nxt:
            # Deterministic Merge (Straight Path)
            straight_paths += 1
            queue.append(nxt)
        else:
            # Logical Bifurcation (Split)
            splits += 1
            new_m = curr.m * 2
            queue.append(MaporaStack(new_m, curr.r, curr.id + "A", curr.layer + 1))
            queue.append(MaporaStack(new_m, curr.r + curr.m, curr.id + "B", curr.layer + 1))
        
        nodes += 1
        
    if splits == 0: return 50.0 # Arbitrary high value for perfect stability
    return straight_paths / splits

# ==========================================
# PART 2: EXPERIMENT - FIBONACCI WEAKNESS
# ==========================================

def run_fibonacci_stress_test():
    print("\n--- EXPERIMENT 1: FIBONACCI STRUCTURAL TENSION ---")
    print(f"{'INDEX':<6} | {'F_VAL':<10} | {'NET SIZE':<10} | {'FIB RATIO':<10} | {'RND RATIO':<10} | {'DELTA'}")
    print("-" * 75)

    a, b = 1, 1
    # Scan Fibonacci numbers F_10 to F_25
    for i in range(3, 26):
        fib_val = a + b
        net_size = 2 ** (fib_val.bit_length())
        
        # 1. Test Fibonacci
        fib_ratio = get_stability_ratio(net_size, fib_val, 400)
        
        # 2. Test Random Control
        rand_val = random.randint(net_size // 2, net_size - 1)
        if rand_val % 2 == 0: rand_val += 1
        rnd_ratio = get_stability_ratio(net_size, rand_val, 400)
        
        delta = fib_ratio - rnd_ratio
        
        # Output
        mark = "⚠️" if delta < -0.15 else ""
        print(f"F_{i:<3} | {fib_val:<10} | 2^{fib_val.bit_length():<2}       | {fib_ratio:<10.4f} | {rnd_ratio:<10.4f} | {delta:+.4f} {mark}")

        a, b = b, fib_val
    print("-" * 75)

# ==========================================
# PART 3: EXPERIMENT - THE HORIZON EVENT
# ==========================================

def run_horizon_scan():
    print("\n--- EXPERIMENT 2: THE HORIZON EVENT (LONGITUDINAL SCAN) ---")
    print("Testing Stability Ratio at Cosmological Scales (up to 2^1000).")
    print(f"{'MAGNITUDE':<15} | {'CONTEXT':<20} | {'STABILITY RATIO'}")
    print("-" * 65)

    scales = [10, 50, 100, 300, 500, 750, 1000]
    
    for bits in scales:
        modulus = 1 << bits
        # Create a hybrid chaos/order residue
        part_a = (1 << bits) - 1
        part_b = random.getrandbits(bits)
        residue = part_a ^ part_b
        if residue % 2 == 0: residue += 1
        
        ratio = get_stability_ratio(modulus, residue, 3000)
        
        context = "Supercomputer" if bits < 70 else "Cosmological" if bits < 300 else "Theoretical"
        bar = "█" * int(ratio * 4)
        print(f"2^{bits:<13} | {context:<20} | {ratio:.4f} {bar}")
        time.sleep(0.1)
    print("-" * 65)

# ==========================================
# PART 4: VISUALIZATION GENERATOR
# ==========================================

def generate_tree_image(residue, mod, title, filename):
    print(f"Generating Image: {filename}...")
    queue = collections.deque([MaporaStack(mod, residue, "R", 0)])
    G = nx.DiGraph()
    G.add_node("R", color='black')
    
    # Depth limited for visual clarity
    while queue:
        curr = queue.popleft()
        if curr.layer >= 14: continue
        nxt = curr.get_next_state()
        
        if nxt:
            G.add_edge(curr.id, nxt.id, color='#2ecc71', weight=2)
            queue.append(nxt)
        else:
            nm = curr.m * 2
            t1 = MaporaStack(nm, curr.r, curr.id + "A", curr.layer + 1)
            t2 = MaporaStack(nm, curr.r + curr.m, curr.id + "B", curr.layer + 1)
            G.add_edge(curr.id, t1.id, color='#e74c3c', weight=1)
            G.add_edge(curr.id, t2.id, color='#e74c3c', weight=1)
            queue.append(t1)
            queue.append(t2)

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    except:
        pos = nx.kamada_kawai_layout(G)

    colors = [G[u][v]['color'] for u, v in G.edges()]
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, edge_color=colors, node_size=20, node_color="black", arrows=False)
    plt.title(title)
    plt.savefig(filename)
    print(f"Saved {filename}")
    plt.close()

# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    print("Initializing Mapora Engine...")
    
    # 1. Run the Fibonacci Analysis (Table 1 in Paper)
    run_fibonacci_stress_test()
    
    # 2. Run the Horizon Scan (Table 2 in Paper)
    run_horizon_scan()
    
    # 3. Generate the Evidence Images
    # Figure 1: Stable Control (Residue 16 on Mod 32)
    generate_tree_image(16, 32, "Figure 1: Normal Residue (Stable)", "Figure1.png")
    
    # Figure 2: The Weakness (Residue 987 on Mod 32)
    generate_tree_image(987, 32, "Figure 2: Fibonacci Residue 987 (Unstable)", "Figure2.png")
    
    print("\nAll tasks complete.")
