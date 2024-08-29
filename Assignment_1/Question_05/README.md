# eulerTotient.py

This script defines two functions for calculating the Euler's totient function `phi` and the greatest common divisor (GCD). The Euler's totient function counts the number of integers up to a given integer \( n \) that are relatively prime to \( n \). 

## Functions

### `gcd(a, b)`
Computes the greatest common divisor of two integers \( a \) and \( b \) using the Euclidean algorithm.

**Parameters:**
- `a` (int): The first integer.
- `b` (int): The second integer.

**Returns:**
- int: The greatest common divisor of \( a \) and \( b \).

### `phi(n)`
Computes the Euler's totient function \(\phi(n)\), which is the number of integers up to \( n \) that are coprime with \( n \).

**Parameters:**
- `n` (int): The integer for which to calculate \(\phi\).

**Returns:**
- int: The value of the Euler's totient function \(\phi(n)\).

## Usage

To use the script, simply run it. The script calculates and prints the Euler's totient function for the integers 30, 100, and 1225.

```python
print(f"30   ==> {phi(30)}")
print(f"100   ==> {phi(100)}")
print(f"1225  ==> {phi(1225)}")
```

## Example Output
When executed, the script produces the following output:

```bash
30   ==> 8
100   ==> 40
1225  ==> 840
```
