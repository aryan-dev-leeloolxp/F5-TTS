#!/usr/bin/env python3
"""
Test script to demonstrate the math text converter functionality.
This script shows examples of mathematical formulas converted to readable text.
"""

from math_text_converter import convert_math_to_speech_text

def print_comparison(original, converted):
    """Print a comparison between original and converted text."""
    print("=" * 80)
    print(f"ORIGINAL: {original}")
    print(f"CONVERTED: {converted}")
    print("-" * 80)

def test_simple_equations():
    """Test conversion of simple equations."""
    examples = [
        "Einstein's famous equation: E = mc²",
        "The Pythagorean theorem states that a² + b² = c²",
        "Newton's second law: F = ma",
        "The Schrödinger equation: iℏ∂Ψ/∂t = ĤΨ",
        "Euler's identity: e^(iπ) + 1 = 0"
    ]
    
    print("\n### SIMPLE EQUATIONS ###")
    for example in examples:
        converted = convert_math_to_speech_text(example)
        print_comparison(example, converted)

def test_advanced_notation():
    """Test conversion of advanced mathematical notation."""
    examples = [
        "The integral ∫(x²+2x+1)dx equals x³/3 + x² + x + C",
        "The gradient is defined as ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)",
        "In quantum mechanics, the uncertainty principle is σₓσₚ ≥ ℏ/2",
        "The probability density function is P(x) = |Ψ(x)|²",
        "For vectors: ||v|| = √(v₁² + v₂² + ... + vₙ²)"
    ]
    
    print("\n### ADVANCED NOTATION ###")
    for example in examples:
        converted = convert_math_to_speech_text(example)
        print_comparison(example, converted)

def test_greek_letters():
    """Test conversion of Greek letters commonly used in mathematics and physics."""
    examples = [
        "The angle θ represents the phase",
        "The coefficient α measures the thermal expansion",
        "The wavelength λ is inversely proportional to frequency",
        "The standard deviation is denoted by σ",
        "In statistics, μ represents the mean of a distribution"
    ]
    
    print("\n### GREEK LETTERS ###")
    for example in examples:
        converted = convert_math_to_speech_text(example)
        print_comparison(example, converted)

def test_complex_expressions():
    """Test conversion of more complex mathematical expressions."""
    examples = [
        "The Fourier transform: F(ω) = ∫f(t)e^(-iωt)dt",
        "The Navier-Stokes equation: ρ(∂v/∂t + v·∇v) = -∇p + μ∇²v + f",
        "Maxwell's equations: ∇·E = ρ/ε₀, ∇×E = -∂B/∂t, ∇·B = 0, ∇×B = μ₀J + μ₀ε₀∂E/∂t",
        "The Einstein field equations: Rμν - (1/2)Rgμν + Λgμν = (8πG/c⁴)Tμν",
        "The heat equation: ∂u/∂t = α∇²u"
    ]
    
    print("\n### COMPLEX EXPRESSIONS ###")
    for example in examples:
        converted = convert_math_to_speech_text(example)
        print_comparison(example, converted)

def test_mixed_text():
    """Test conversion of text with mixed content (mathematical and non-mathematical)."""
    examples = [
        "The Riemann Hypothesis states that all non-trivial zeros of ζ(s) have real part 1/2.",
        "In physics, E = mc² relates energy (E) to mass (m) multiplied by the speed of light (c) squared.",
        "The function f(x) = x² + 2x + 1 can be factored as (x+1)².",
        "For a circle with radius r, the area is πr² and the circumference is 2πr.",
        "The standard normal distribution has μ = 0 and σ = 1, with probability density function f(x) = (1/√(2π))e^(-(x²)/2)."
    ]
    
    print("\n### MIXED TEXT ###")
    for example in examples:
        converted = convert_math_to_speech_text(example)
        print_comparison(example, converted)

def test_real_world_examples():
    """Test with real-world examples from scientific papers or textbooks."""
    examples = [
        "According to general relativity, the curvature of spacetime is given by Rᵤᵥ - (1/2)Rg_μν = (8πG/c⁴)T_μν",
        "Core equations studied:• H = -ℏ²/2m ∇² + V • ∫(x²+2x+1)dx = x³/3 + x² + x + C• F = ma = m(d²x/dt²)",
        "Statistical significance was achieved (p < 0.05) across all experimental conditions (χ² = 12.4).",
        "The wave function collapse in quantum mechanics leads to Ψ → |a⟩ with probability |⟨a|Ψ⟩|²",
        "In economics, the Gini coefficient G = 2∫₀¹[p - L(p)]dp measures income inequality.",
        "The black-hole entropy is given by S = kₑA/4ℓₚ², where A is the event horizon area."
    ]
    
    print("\n### REAL-WORLD EXAMPLES ###")
    for example in examples:
        converted = convert_math_to_speech_text(example)
        print_comparison(example, converted)

def main():
    """Run all test cases."""
    print("TESTING MATH TEXT CONVERTER")
    print("==========================")
    
    # test_simple_equations()
    # test_advanced_notation()
    # test_greek_letters()
    # test_complex_expressions()
    # test_mixed_text()
    test_real_world_examples()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    main() 