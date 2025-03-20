#!/usr/bin/env python3
"""
Mathematical formula to readable text converter for TTS systems.
This module converts mathematical notations into TTS-friendly English text.
"""

import re
import unicodedata
import argparse
import sys


class MathTextConverter:
    """Convert mathematical formulas to readable English text."""
    
    def __init__(self):
        """Initialize the converter with conversion rules."""
        # Symbol mappings
        self.symbol_map = {
            # Greek letters
            'α': 'alpha',
            'β': 'beta',
            'γ': 'gamma',
            'Γ': 'capital gamma',
            'δ': 'delta',
            'Δ': 'capital delta',
            'ε': 'epsilon',
            'ζ': 'zeta',
            'η': 'eta',
            'θ': 'theta',
            'Θ': 'capital theta',
            'ι': 'iota',
            'κ': 'kappa',
            'λ': 'lambda',
            'Λ': 'capital lambda',
            'μ': 'mu',
            'ν': 'nu',
            'ξ': 'xi',
            'Ξ': 'capital xi',
            'π': 'pi',
            'Π': 'capital pi',
            'ρ': 'rho',
            'σ': 'sigma',
            'Σ': 'capital sigma',
            'τ': 'tau',
            'υ': 'upsilon',
            'φ': 'phi',
            'Φ': 'capital phi',
            'χ': 'chi',
            'ψ': 'psi',
            'Ψ': 'capital psi',
            'ω': 'omega',
            'Ω': 'capital omega',
            
            # Mathematical operators and symbols
            '∫': 'integral of',
            '∇': 'del',
            '∂': 'partial derivative of',
            '±': 'plus or minus',
            '×': 'times',
            '÷': 'divided by',
            '≈': 'approximately equal to',
            '≠': 'not equal to',
            '≤': 'less than or equal to',
            '≥': 'greater than or equal to',
            '→': 'approaches',
            '↑': 'up arrow',
            '↓': 'down arrow',
            '⊆': 'is a subset of',
            '⊂': 'is a proper subset of',
            '∈': 'is an element of',
            '∉': 'is not an element of',
            '∩': 'intersection',
            '∪': 'union',
            '∞': 'infinity',
            '∝': 'proportional to',
            '∑': 'sum of',
            '∏': 'product of',
            '√': 'square root of',
            'ℝ': 'the set of real numbers',
            'ℤ': 'the set of integers',
            'ℕ': 'the set of natural numbers',
            'ℚ': 'the set of rational numbers',
            'ℂ': 'the set of complex numbers',
            '∠': 'angle',
            '°': 'degrees',
            '∅': 'empty set',
            '∀': 'for all',
            '∃': 'there exists',
            '¬': 'not',
            '∧': 'and',
            '∨': 'or',
            '⊕': 'direct sum',
            '⊗': 'tensor product',
            '⇒': 'implies',
            '⇔': 'if and only if',
            '|': 'such that',
            '||': 'norm of',
            '‖': 'norm of',
            '′': 'prime',
            '″': 'double prime',
            '‴': 'triple prime',
            'ℏ': 'h-bar',
            
            # Common subscripts/superscripts
            '²': ' squared',
            '³': ' cubed',
            '⁴': ' to the fourth power',
            '⁵': ' to the fifth power',
            '⁶': ' to the sixth power',
            '⁷': ' to the seventh power',
            '⁸': ' to the eighth power',
            '⁹': ' to the ninth power',
            '⁰': ' to the power of zero',
            '₁': ' sub one',
            '₂': ' sub two',
            '₃': ' sub three',
            '₄': ' sub four',
            '₅': ' sub five',
            '₆': ' sub six',
            '₇': ' sub seven',
            '₈': ' sub eight',
            '₉': ' sub nine',
            '₀': ' sub zero',
            
            # Musical and other notations
            '♭': 'flat',
            '♯': 'sharp',
            '♮': 'natural',
            '♩': 'quarter note',
            '♪': 'eighth note',
            '♫': 'musical notes',
            '♬': 'musical notes',
            '𝄇': 'repeat',
            '𝄞': 'treble clef',
            
            # Other special characters
            '…': 'ellipsis',
        }
        
        # Pattern for identifying complex mathematical expressions
        self.math_patterns = [
            (r'd(\^?)(\d+)x/dt(\^?)(\d+)', r'the \2 derivative of x with respect to t\4'),
            (r'f\(x\)', 'f of x'),
            (r'O\(([^)]+)\)', r'big O of \1'),
            (r'([a-zA-Z])\^(\d+)', r'\1 to the \2 power'),
            (r'([a-zA-Z])_(\d+)', r'\1 sub \2'),
            (r'([a-zA-Z]+)\(([a-zA-Z])\)', r'\1 of \2'),
            (r'\\int', 'integral'),
            (r'\\sum', 'sum'),
            (r'\\product', 'product'),
            (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 divided by \2'),
            (r'\\sqrt\{([^}]+)\}', r'square root of \1'),
            (r'\\Delta', 'Delta'),
        ]
        
        # Add LaTeX command mappings
        self.latex_commands = {
            r'\\alpha': 'alpha',
            r'\\beta': 'beta',
            r'\\gamma': 'gamma',
            r'\\Gamma': 'capital gamma',
            r'\\delta': 'delta',
            r'\\Delta': 'capital delta',
            r'\\epsilon': 'epsilon',
            r'\\varepsilon': 'epsilon',
            r'\\zeta': 'zeta',
            r'\\eta': 'eta',
            r'\\theta': 'theta',
            r'\\Theta': 'capital theta',
            r'\\iota': 'iota',
            r'\\kappa': 'kappa',
            r'\\lambda': 'lambda',
            r'\\Lambda': 'capital lambda',
            r'\\mu': 'mu',
            r'\\nu': 'nu',
            r'\\xi': 'xi',
            r'\\Xi': 'capital xi',
            r'\\pi': 'pi',
            r'\\Pi': 'capital pi',
            r'\\rho': 'rho',
            r'\\sigma': 'sigma',
            r'\\Sigma': 'capital sigma',
            r'\\tau': 'tau',
            r'\\upsilon': 'upsilon',
            r'\\phi': 'phi',
            r'\\Phi': 'capital phi',
            r'\\chi': 'chi',
            r'\\psi': 'psi',
            r'\\Psi': 'capital psi',
            r'\\omega': 'omega',
            r'\\Omega': 'capital omega',
            r'\\int': 'integral of',
            r'\\oint': 'contour integral of',
            r'\\nabla': 'del',
            r'\\partial': 'partial derivative of',
            r'\\pm': 'plus or minus',
            r'\\times': 'times',
            r'\\div': 'divided by',
            r'\\approx': 'approximately equal to',
            r'\\neq': 'not equal to',
            r'\\leq': 'less than or equal to',
            r'\\geq': 'greater than or equal to',
            r'\\rightarrow': 'approaches',
            r'\\to': 'approaches',
            r'\\subset': 'is a proper subset of',
            r'\\subseteq': 'is a subset of',
            r'\\in': 'is an element of',
            r'\\notin': 'is not an element of',
            r'\\cap': 'intersection',
            r'\\cup': 'union',
            r'\\infty': 'infinity',
            r'\\propto': 'proportional to',
            r'\\sum': 'sum of',
            r'\\prod': 'product of',
            r'\\sqrt': 'square root of',
            r'\\mathbb\{R\}': 'the set of real numbers',
            r'\\mathbb\{Z\}': 'the set of integers',
            r'\\mathbb\{N\}': 'the set of natural numbers',
            r'\\mathbb\{Q\}': 'the set of rational numbers',
            r'\\mathbb\{C\}': 'the set of complex numbers',
            r'\\angle': 'angle',
            r'\\emptyset': 'empty set',
            r'\\forall': 'for all',
            r'\\exists': 'there exists',
            r'\\neg': 'not',
            r'\\wedge': 'and',
            r'\\vee': 'or',
            r'\\oplus': 'direct sum',
            r'\\otimes': 'tensor product',
            r'\\Rightarrow': 'implies',
            r'\\Leftrightarrow': 'if and only if',
            r'\\hbar': 'h-bar',
            r'\\cdot': 'dot',
            r'\\frac': 'fraction',
            r'\\sqrt': 'square root of',
            r'\\sin': 'sine',
            r'\\cos': 'cosine',
            r'\\tan': 'tangent',
            r'\\cot': 'cotangent',
            r'\\sec': 'secant',
            r'\\csc': 'cosecant',
            r'\\log': 'logarithm',
            r'\\ln': 'natural logarithm',
            r'\\exp': 'exponential function',
            r'\\lim': 'limit',
            r'\\infty': 'infinity',
            r'\\therefore': 'therefore',
            r'\\because': 'because',
            r'\\ldots': 'dots',
            r'\\cdots': 'center dots',
            r'\\vdots': 'vertical dots',
            r'\\ddots': 'diagonal dots',
        }

    def _replace_simple_symbols(self, text):
        """Replace simple mathematical symbols with their text representations."""
        for symbol, replacement in self.symbol_map.items():
            text = text.replace(symbol, f" {replacement} ")
        return text

    def _process_complex_expressions(self, text):
        """Process more complex mathematical expressions using regex patterns."""
        for pattern, replacement in self.math_patterns:
            text = re.sub(pattern, replacement, text)
        return text

    def _handle_specific_equations(self, text):
        """Handle specific common equations with custom replacements."""
        # Specific equation patterns
        equations = {
            r'E\s*=\s*mc²': "E equals m c squared",
            r'F\s*=\s*ma': "Force equals mass times acceleration",
            r'a²\s*\+\s*b²\s*=\s*c²': "a squared plus b squared equals c squared",
            r'E\s*=\s*hν': "E equals h nu",
            r'PV\s*=\s*nRT': "P V equals n R T",
            r'e\^?\{\s*i\s*\\\s*pi\s*\}\s*\+\s*1\s*=\s*0': "e to the power of i pi plus 1 equals 0",
        }
        
        for pattern, replacement in equations.items():
            text = re.sub(pattern, replacement, text)
        
        return text

    def _clean_spacing(self, text):
        """Clean up extra spaces and format the text."""
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Fix spacing around punctuation
        text = re.sub(r'\s([,.;:!?])', r'\1', text)
        return text.strip()

    def _handle_fractions(self, text):
        """Handle mathematical fractions."""
        # Pattern for fractions like x/y
        fraction_pattern = r'(\w+)/(\w+)'
        text = re.sub(fraction_pattern, r'\1 divided by \2', text)
        
        # Handle more complex fractions
        text = re.sub(r'(\w+)\s*/\s*(\w+)', r'\1 divided by \2', text)
        
        return text

    def _handle_square_roots(self, text):
        """Handle square root notation."""
        # Basic square root pattern
        sqrt_pattern = r'√\s*(\w+)'
        text = re.sub(sqrt_pattern, r'square root of \1', text)
        
        return text

    def _handle_powers_and_subscripts(self, text):
        """Handle powers and subscripts that are written with ^ and _."""
        # Powers with caret notation
        text = re.sub(r'(\w+)\^(\w+)', r'\1 to the power of \2', text)
        
        # Subscripts with underscore notation
        text = re.sub(r'(\w+)_(\w+)', r'\1 sub \2', text)
        
        return text
        
    def _handle_latex_commands(self, text):
        """Handle LaTeX commands and expressions."""
        # Replace common LaTeX commands
        for pattern, replacement in self.latex_commands.items():
            text = re.sub(pattern, f" {replacement} ", text)
        
        # Handle LaTeX superscripts (e.g., x^{2} or x^2)
        text = re.sub(r'(\w+)\^\{(\w+)\}', r'\1 to the power of \2', text)
        text = re.sub(r'(\w+)\^(\w)', r'\1 to the power of \2', text)
        
        # Handle LaTeX subscripts (e.g., x_{i} or x_i)
        text = re.sub(r'(\w+)_\{(\w+)\}', r'\1 sub \2', text)
        text = re.sub(r'(\w+)_(\w)', r'\1 sub \2', text)
        
        # Handle LaTeX fractions
        text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 divided by \2', text)
        
        # Handle LaTeX roots
        text = re.sub(r'\\sqrt\{([^}]+)\}', r'square root of \1', text)
        text = re.sub(r'\\sqrt\[(\d+)\]\{([^}]+)\}', r'the \1 root of \2', text)
        
        # Handle math delimiters
        text = re.sub(r'\$\$(.*?)\$\$', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'\$(.*?)\$', r'\1', text)
        text = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'\\begin\{align\}(.*?)\\end\{align\}', r'\1', text, flags=re.DOTALL)
        
        # Handle LaTeX matrices
        text = re.sub(r'\\begin\{matrix\}(.*?)\\end\{matrix\}', r'matrix \1', text, flags=re.DOTALL)
        text = re.sub(r'\\\\', r' next row ', text)
        text = re.sub(r'&', r' column ', text)
        
        return text

    def _handle_operators(self, text):
        """Handle mathematical operators and equality symbols."""
        # Replace common operators
        operators = {
            r'=': ' equals ',
            r'\+': ' plus ',
            r'-': ' minus ',
            r'\*': ' times ',
            r'==': ' equals ',
            r'!=': ' not equal to ',
            r'<': ' less than ',
            r'>': ' greater than ',
            r'<=': ' less than or equal to ',
            r'>=': ' greater than or equal to ',
        }
        
        for pattern, replacement in operators.items():
            # Only replace when they're used as operators (with space around them)
            text = re.sub(r'(\s)' + pattern + r'(\s)', r'\1' + replacement + r'\2', text)
            
            # Also replace at the beginning of a string
            text = re.sub(r'^' + pattern + r'(\s)', replacement + r'\1', text)
            
            # And at the end of a string
            text = re.sub(r'(\s)' + pattern + r'$', r'\1' + replacement, text)
        
        return text

    def convert(self, text):
        """
        Convert mathematical formulas in text to readable English.
        
        Args:
            text (str): Text containing mathematical formulas
            
        Returns:
            str: Text with mathematical formulas converted to readable English
        """
        # Make a copy of the original text
        converted_text = text
        
        # Apply conversions in sequence
        converted_text = self._handle_latex_commands(converted_text)
        converted_text = self._replace_simple_symbols(converted_text)
        converted_text = self._process_complex_expressions(converted_text)
        converted_text = self._handle_specific_equations(converted_text)
        converted_text = self._handle_fractions(converted_text)
        converted_text = self._handle_square_roots(converted_text)
        converted_text = self._handle_powers_and_subscripts(converted_text)
        converted_text = self._handle_operators(converted_text)
        
        # Clean up the text
        converted_text = self._clean_spacing(converted_text)
        
        return converted_text


def convert_math_to_speech_text(text):
    """
    Convert mathematical formulas in text to TTS-friendly format.
    
    Args:
        text (str): Input text with mathematical formulas
        
    Returns:
        str: Text with mathematical formulas converted to readable text
    """
    converter = MathTextConverter()
    return converter.convert(text)


def process_file(input_file, output_file=None):
    """
    Process an entire file, converting mathematical formulas to readable text.
    
    Args:
        input_file (str): Path to input file
        output_file (str, optional): Path to output file. If None, print to stdout.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        converted = convert_math_to_speech_text(content)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"Converted text saved to: {output_file}")
        else:
            print(converted)
            
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert mathematical formulas to readable text for TTS')
    parser.add_argument('input', nargs='?', help='Input text or file path (if --file flag is used)')
    parser.add_argument('-f', '--file', action='store_true', help='Treat the input as a file path')
    parser.add_argument('-o', '--output', help='Output file path (optional, stdout if not provided)')
    
    if len(sys.argv) == 1:
        # If no arguments provided, run the demo
        test_texts = [
            "The equation E = mc² is famous.",
            "The integral ∫(x²+2x+1)dx equals x³/3 + x² + x + C",
            "The Schrödinger equation is H = -ℏ²/2m ∇² + V",
            "For a sphere, V = 4/3πr³",
            "The eigenvalues λᵢ satisfy det(A - λI) = 0",
            "LaTeX example: $\\frac{\\partial^2 u}{\\partial t^2} = c^2 \\nabla^2 u$"
        ]
        
        converter = MathTextConverter()
        print("=== Math Text Converter Demo ===")
        for test in test_texts:
            converted = converter.convert(test)
            print(f"Original: {test}")
            print(f"Converted: {converted}")
            print("-" * 80)
    else:
        args = parser.parse_args()
        
        if args.file:
            if not args.input:
                print("Error: Input file path is required when using --file flag", file=sys.stderr)
                sys.exit(1)
            process_file(args.input, args.output)
        else:
            if args.input:
                converted = convert_math_to_speech_text(args.input)
                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(converted)
                    print(f"Converted text saved to: {args.output}")
                else:
                    print(converted)
            else:
                print("Error: Input text is required", file=sys.stderr)
                sys.exit(1) 