#!/usr/bin/env python3
"""
Script to generate a .clc file with current loop entries from 1 to 89
"""

def generate_clc_file(output_filename='current_loops.clc', start=1, end=89):
    """
    Generate a .clc file with named expressions for current loops
    
    Args:
        output_filename: Name of the output .clc file
        start: Starting loop number (default: 1)
        end: Ending loop number (default: 89)
    """
    
    with open(output_filename, 'w') as f:
        for i in range(start, end + 1):
            # Real part expression
            f.write("$begin 'Named_Expression'\n")
            f.write(f"Name('current_loop_1_{i}_real')\n")
            f.write(f"Expression('Integrate(Line(current_loop_1_{i}), Dot(Real(<Hx,Hy,Hz>), LineTangent))')\n")
            f.write("NameOfExpression('<Hx,Hy,Hz>')\n")
            f.write("Operation('Real')\n")
            f.write("Operation('Tangent')\n")
            f.write("Operation('Dot')\n")
            f.write(f"EnterLine('current_loop_1_{i}')\n")
            f.write("Operation('LineValue')\n")
            f.write("Operation('Integrate')\n")
            f.write("$end 'Named_Expression'\n")
            
            # Imaginary part expression
            f.write("$begin 'Named_Expression'\n")
            f.write(f"Name('current_loop_1_{i}_imag')\n")
            f.write(f"Expression('Integrate(Line(current_loop_1_{i}), Dot(Imag(<Hx,Hy,Hz>), LineTangent))')\n")
            f.write("NameOfExpression('<Hx,Hy,Hz>')\n")
            f.write("Operation('Imag')\n")
            f.write("Operation('Tangent')\n")
            f.write("Operation('Dot')\n")
            f.write(f"EnterLine('current_loop_1_{i}')\n")
            f.write("Operation('LineValue')\n")
            f.write("Operation('Integrate')\n")
            f.write("$end 'Named_Expression'\n")
    
    print(f"Successfully generated {output_filename} with {(end - start + 1) * 2} named expressions")
    print(f"Range: current_loop_{start} to current_loop_{end}")

if __name__ == "__main__":
    # Generate the .clc file
    generate_clc_file('current_loops.clc', start=1, end=89)
