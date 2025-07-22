#!/usr/bin/env python3
"""
Measure optimized log volume compared to baseline
"""

import subprocess
import sys
import time
import signal
from pathlib import Path

def measure_optimized_startup():
    """Start server and capture optimized logs for comparison."""
    print("📊 Measuring optimized startup log volume...")
    
    try:
        # Start server and capture logs for 30 seconds
        process = subprocess.Popen(
            ["uv", "run", "python", "api/serve.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            preexec_fn=os.setsid if hasattr(__import__('os'), 'setsid') else None
        )
        
        logs = []
        start_time = time.time()
        
        print("⏳ Capturing logs for 30 seconds...")
        while time.time() - start_time < 30:
            line = process.stdout.readline()
            if line:
                logs.append(line.strip())
                # Print progress every 5 seconds
                elapsed = time.time() - start_time
                if int(elapsed) % 5 == 0 and len(logs) % 10 == 0:
                    print(f"   📝 Captured {len(logs)} lines in {elapsed:.0f}s")
            else:
                # Process ended early
                break
                
        # Terminate process gracefully
        try:
            if hasattr(process, 'terminate'):
                process.terminate()
                process.wait(timeout=5)
        except (subprocess.TimeoutExpired, ProcessLookupError):
            try:
                process.kill()
            except ProcessLookupError:
                pass
        
        return [log for log in logs if log.strip()]
        
    except KeyboardInterrupt:
        print("\n⚠️ Measurement interrupted by user")
        if 'process' in locals():
            try:
                process.terminate()
            except:
                pass
        return []
    except Exception as e:
        print(f"❌ Error measuring logs: {e}")
        return []

def compare_with_baseline():
    """Compare optimized logs with baseline."""
    print("🔍 Comparing optimized logs with baseline...")
    
    # Load baseline
    baseline_file = Path("baseline_logs.txt")
    if not baseline_file.exists():
        print("❌ baseline_logs.txt not found. Run measure_log_volume.py first.")
        return False
        
    with open(baseline_file) as f:
        baseline_logs = [line.strip() for line in f if line.strip()]
    
    baseline_count = len(baseline_logs)
    print(f"📋 Baseline log lines: {baseline_count}")
    
    # Measure optimized logs
    optimized_logs = measure_optimized_startup()
    optimized_count = len(optimized_logs)
    
    if optimized_count == 0:
        print("❌ No optimized logs captured")
        return False
        
    print(f"📋 Optimized log lines: {optimized_count}")
    
    # Calculate improvement
    if baseline_count > 0:
        reduction = ((baseline_count - optimized_count) / baseline_count) * 100
        print(f"📉 Log volume reduction: {reduction:.1f}%")
        
        target_reduction = 60
        if reduction >= target_reduction:
            print(f"🎉 SUCCESS: Exceeded {target_reduction}% reduction target!")
        else:
            print(f"⚠️ TARGET MISSED: Only {reduction:.1f}% reduction (target: {target_reduction}%)")
    else:
        print("❌ Cannot calculate reduction with empty baseline")
        return False
    
    # Save optimized logs for analysis
    with open("optimized_logs.txt", "w") as f:
        for log in optimized_logs:
            f.write(f"{log}\n")
    print("💾 Optimized logs saved to optimized_logs.txt")
    
    # Show sample comparison
    print("\n📊 SAMPLE COMPARISON:")
    print("=" * 50)
    print("🔸 BASELINE (first 10 lines):")
    for i, line in enumerate(baseline_logs[:10]):
        print(f"  {i+1:2d}: {line[:100]}")
    
    print("\n🔹 OPTIMIZED (first 10 lines):")
    for i, line in enumerate(optimized_logs[:10]):
        print(f"  {i+1:2d}: {line[:100]}")
    
    return reduction >= target_reduction

def main():
    """Main comparison function."""
    print("🚀 Log Optimization Validation")
    print("=" * 40)
    
    success = compare_with_baseline()
    
    if success:
        print("\n✅ LOG OPTIMIZATION SUCCESSFUL!")
        print("📈 Target reduction achieved")
        print("🎯 Clean, informative logs maintained")
    else:
        print("\n❌ LOG OPTIMIZATION NEEDS ADJUSTMENT") 
        print("📋 Review logs and adjust batch thresholds")
    
    return success

if __name__ == "__main__":
    import os
    success = main()
    sys.exit(0 if success else 1)