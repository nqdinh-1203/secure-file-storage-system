import random

'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''


def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


'''
Tests to see if a number is prime.
'''


def is_prime(n, k):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


"""
a function that uses miller rabin's primality test to genarate a prime number in a certain number of bits length
in other words you give it a number of bits and you will get a prime number with that number of bits
"""


def prime_gen(bits):
    x = ""
    bits = int(bits)
    for y in range(bits):
        x = x + "1"
    y = "1"
    for z in range(bits - 1):
        y = y + "0"
    x = int(x, 2)
    y = int(y, 2)
    p = 0
    while True:
        p = random.randrange(y, x)
        if is_prime(p, 40):
            break
    return p


def key_gen(bits):
    p = prime_gen(bits)
    q = prime_gen(bits)

    while p == q:
        p = prime_gen(bits)
        q = prime_gen(bits)

    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private key_pair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(publickey, plaintext) -> int():
    # Unpack the key into it's components
    e, n = publickey
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = pow(int(plaintext), e, n)
    # Return the array of bytes
    return cipher


def decrypt(privatekey, ciphertext) -> int():
    # Unpack the key into its components
    d, n = privatekey
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plaintext = pow(int(ciphertext), d, n)
    # Return the array of bytes as a string
    return plaintext
