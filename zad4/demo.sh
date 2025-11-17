#!/bin/bash

# Demo script for C_3 cycle detection
# Shows all implemented features

echo "========================================="
echo "C_3 CYCLE DETECTION - DEMO"
echo "========================================="
echo ""

echo "1. Simple triangle (both methods)"
echo "-----------------------------------"
python main.py graphs/triangle.txt
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "2. Graph without triangles"
echo "-----------------------------------"
python main.py graphs/no_triangles.txt
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "3. Complete graph K4 - show all triangles"
echo "-----------------------------------"
python main.py graphs/complete_k4.txt --show-all
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "4. Matrix multiplication demonstration"
echo "-----------------------------------"
python main.py graphs/triangle.txt --demo
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "5. Directed graph with cycle"
echo "-----------------------------------"
python main.py graphs/directed_cycle.txt --verbose
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "6. Benchmark comparison"
echo "-----------------------------------"
python main.py graphs/multiple_triangles.txt --benchmark --show-all
echo ""

echo "========================================="
echo "Demo complete!"
echo "========================================="

