#!/bin/bash

# Define the classes you want to run
classes=("A" "B" "C" "D")

# Loop through each class and run the CG benchmark
for class in "${classes[@]}"
do
    echo "========================================"
    echo "Running CG Benchmark for Class $class"
    echo "========================================"

    # Compile the CG kernel for the current class
    make clean  # Clean previous builds
    make cg CLASS=$class

    # Check if compilation was successful
    if [ $? -eq 0 ]; then
        echo "Compilation successful. Running CG kernel for Class $class..."
        # Run the CG kernel (adjust path if needed)
        ./bin/cg.$class
    else
        echo "Compilation failed for Class $class."
        exit 1
    fi

    echo ""
done
