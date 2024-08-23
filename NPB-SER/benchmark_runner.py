import subprocess
import re
import os

def run_benchmark(benchmark_class, n_runs, thread_nums):
    # Compile the benchmark once
    compile_command = f"make cg CLASS={benchmark_class}"
    subprocess.run(compile_command, shell=True, check=True)

    for thread_num in thread_nums:
        times = []
        verification_successful = True

        # Set the number of threads
        os.environ["OMP_NUM_THREADS"] = str(thread_num)
        print(f"\nRunning benchmark with {thread_num} threads...")

        # Run the benchmark n_runs times
        for i in range(n_runs):
            run_command = f"./bin/cg.{benchmark_class}"
            result = subprocess.run(run_command, shell=True, capture_output=True, text=True)

            # Extract the execution time from the output
            time_match = re.search(r"Time in seconds\s+=\s+(\d+\.\d+)", result.stdout)
            verification_match = re.search(r"Verification\s+=\s+(SUCCESSFUL|UNSUCCESSFUL)", result.stdout)

            if time_match:
                time = float(time_match.group(1))
                times.append(time)
                print(f"Run {i + 1} with {thread_num} threads: {time} seconds")
            else:
                print("Error: Execution time not found in output.")

            # Check verification status
            if verification_match:
                verification_status = verification_match.group(1)
                if verification_status == "UNSUCCESSFUL":
                    verification_successful = False
                    print(f"Warning: Run {i + 1} with {thread_num} threads - Verification UNSUCCESSFUL")

        # Calculate and print the mean execution time for the current thread count
        if times:
            mean_time = sum(times) / len(times)
            print(f"\nMean execution time with {thread_num} threads after {n_runs} runs: {mean_time:.2f} seconds")
        else:
            print(f"Error: No valid execution times recorded for {thread_num} threads.")

        # Final verification status
        if not verification_successful:
            print(f"\nWARNING: One or more runs with {thread_num} threads had UNSUCCESSFUL verification.")
        else:
            print(f"\nAll runs with {thread_num} threads had SUCCESSFUL verification.")

if __name__ == "__main__":
    benchmark_class = input("Enter benchmark CLASS (A, B, C, D, E, F): ").strip()
    n_runs = int(input("Enter the number of runs (nRuns): "))
    thread_nums = list(map(int, input("Enter the number of threads (thread_num) as space-separated values: ").split()))

    run_benchmark(benchmark_class, n_runs, thread_nums)
