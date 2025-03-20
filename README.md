# F5-TTS Mathematical Formula Converter

A Python utility for converting mathematical formulas and notations into TTS-friendly readable text for the F5-TTS text-to-speech synthesis system.

## Overview

This tool solves the common problem of Text-to-Speech (TTS) systems struggling to properly pronounce mathematical formulas, equations, and special notations. It converts mathematical expressions into natural language that TTS systems can read correctly.

## Features

- Converts Unicode mathematical symbols to readable text
- Handles Greek letters (α, β, γ, etc.)
- Processes LaTeX expressions and commands
- Converts superscripts/subscripts (², ₃, etc.)
- Interprets common mathematical operators (∫, ∇, ∂, etc.)
- Handles fractions, square roots, and other special notations
- Support for specific common equations (E=mc², Pythagorean theorem, etc.)
- Command-line interface for processing individual text inputs or entire files

## Installation

No installation required. Just clone the repository and ensure you have Python 3.6+ installed.

## Usage

### As a Python Module

```python
from math_text_converter import convert_math_to_speech_text

# Convert text with mathematical formulas
original_text = "The equation E = mc² describes the equivalence of mass and energy."
tts_friendly_text = convert_math_to_speech_text(original_text)
print(tts_friendly_text)
# Output: "The equation E equals m c squared describes the equivalence of mass and energy."
```

### With F5-TTS Sample Script

The sample script integrates the math converter with F5-TTS:

```python
# Run TTS with math formula conversion
run_tts(complex_text, "output.wav", convert_math=True)
```

### Command Line Usage

```bash
# Display demo examples
python math_text_converter.py

# Convert a single text string
python math_text_converter.py "The integral ∫(x²+2x+1)dx equals x³/3 + x² + x + C"

# Process an entire file
python math_text_converter.py -f input.txt -o output.txt
```

## Examples

Original: The Schrödinger equation is H = -ℏ²/2m ∇² + V
Converted: The Schrödinger equation is H equals minus h-bar squared divided by 2m del squared plus V

Original: For vectors: ||v|| = √(v₁² + v₂² + ... + vₙ²)
Converted: For vectors: norm of v equals square root of v sub one squared plus v sub two squared plus ellipsis plus v sub n squared

Original: LaTeX example: $\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u$
Converted: LaTeX example: partial derivative of squared u divided by partial derivative of t squared equals c squared del squared u

## Test Script

You can use the included `test_math_converter.py` script to see various examples of formula conversions.

```bash
python test_math_converter.py
```

## Files

- `math_text_converter.py` - Core conversion library and command-line interface
- `sample_tts.py` - Integration with F5-TTS system
- `test_math_converter.py` - Examples and test cases
- `README.md` - Documentation

## Future Improvements

- Add support for chemical formulas and equations
- Improve handling of complex LaTeX expressions
- Add support for more languages and internationalization
- Implement MathML parsing
- Add support for common physics and engineering formulas

## License

MIT
