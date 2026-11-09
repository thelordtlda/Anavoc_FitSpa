import subprocess
import sys
import time

brands = [
    "Caldera Spas",
    "Coast Spas",
    "Marquis Spas",
    "Hydropool",
    "Beachcomber",
    "Arctic Spas",
    "Cal Spas"
]

python_exe = sys.executable

print("======================================================================")
print("              WAYBACK HARVESTER CAMPAIGN: BATCH #6                    ")
print("======================================================================")

total_start = time.time()
for b in brands:
    print(f"\n>>> STARTING BATCH #6 HARVEST FOR: {b} <<<")
    cmd = [python_exe, "scripts/wayback_generational_harvester.py", "--brand", b, "--limit", "15", "--commit"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(res.stdout)
        if res.stderr:
            print("STDERR:", res.stderr)
    except subprocess.TimeoutExpired:
        print(f"Brand {b} timed out after 300s.")
    except Exception as e:
        print(f"Error running {b}: {e}")

print(f"\n[DONE] Batch #6 Campaign completed in {time.time() - total_start:.1f}s.")
