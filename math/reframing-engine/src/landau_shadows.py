"""Finite shadows for Landau n^2+1. Every integer this file prints is computed here.

Timeouts: every loop checks a deadline. On timeout raise TimeoutError; never guess.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Iterable


HARD_TIMEOUT_SEC = 30.0


class Timeout(Exception):
    pass


def _deadline(seconds: float | None = None) -> float:
    return time.time() + (seconds if seconds is not None else HARD_TIMEOUT_SEC)


def _check(deadline: float) -> None:
    if time.time() > deadline:
        raise Timeout("landau shadow timed out")


def sieve_primes(limit: int, deadline: float | None = None) -> list[int]:
    dl = deadline if deadline is not None else _deadline()
    if limit < 2:
        return []
    marks = bytearray(b"\x01") * (limit + 1)
    marks[0] = marks[1] = 0
    r = int(limit**0.5)
    for p in range(2, r + 1):
        _check(dl)
        if marks[p]:
            step = p
            start = p * p
            marks[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return [i for i, v in enumerate(marks) if v]


def is_prime(n: int, primes: Iterable[int] | None = None) -> bool:
    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0:
        return False
    if primes is None:
        r = int(n**0.5)
        d = 3
        while d <= r:
            if n % d == 0:
                return False
            d += 2
        return True
    r = int(n**0.5)
    for p in primes:
        if p > r:
            break
        if n % p == 0:
            return False
    return True


def chi4(n: int) -> int:
    r = n % 4
    if r == 1:
        return 1
    if r == 3:
        return -1
    return 0


@dataclass(frozen=True)
class Census:
    n_max: int
    prime_values: int
    first_n: tuple[int, ...]
    odd_n_primes: int


def census_n2plus1(n_max: int, deadline: float | None = None) -> Census:
    dl = deadline if deadline is not None else _deadline()
    # n^2+1 <= n_max^2+1, sieve up to that.
    limit = n_max * n_max + 1
    primes = sieve_primes(limit, dl)
    prime_set = set(primes)
    count = 0
    first: list[int] = []
    odd_primes = 0
    for n in range(1, n_max + 1):
        _check(dl)
        val = n * n + 1
        if val in prime_set:
            count += 1
            if len(first) < 20:
                first.append(n)
            if n % 2 == 1:
                odd_primes += 1
    return Census(n_max, count, tuple(first), odd_primes)


def odd_prime_factors_mod4(n_max: int, deadline: float | None = None) -> bool:
    """Return True iff every odd prime factor of n^2+1 for n<=n_max is 1 mod 4."""
    dl = deadline if deadline is not None else _deadline()
    limit = n_max * n_max + 1
    primes = sieve_primes(int(limit**0.5) + 10, dl)
    for n in range(1, n_max + 1):
        _check(dl)
        m = n * n + 1
        for p in primes:
            if p * p > m:
                break
            if m % p == 0:
                if p != 2 and p % 4 != 1:
                    return False
                while m % p == 0:
                    m //= p
        if m > 1 and m != 2 and m % 4 != 1:
            return False
    return True


def omega_parity(n_max: int, deadline: float | None = None) -> tuple[int, int, int, int, int, int]:
    """Return (omega1, omega2, omega3, omega_ge4, odd_omega, even_omega). Full factorization."""
    dl = deadline if deadline is not None else _deadline()
    limit = n_max * n_max + 1
    primes = sieve_primes(int(limit**0.5) + 20, dl)
    c1 = c2 = c3 = cge4 = odd = even = 0
    for n in range(1, n_max + 1):
        _check(dl)
        m = n * n + 1
        omega = 0
        for p in primes:
            if p * p > m:
                break
            while m % p == 0:
                omega += 1
                m //= p
        if m > 1:
            omega += 1
        if omega == 1:
            c1 += 1
        elif omega == 2:
            c2 += 1
        elif omega == 3:
            c3 += 1
        else:
            cge4 += 1
        if omega % 2:
            odd += 1
        else:
            even += 1
    return c1, c2, c3, cge4, odd, even


def bateman_horn_truncated(prime_bound: int, deadline: float | None = None) -> float:
    """C_B = prod_{3<=p<=B} (1 - chi4(p)/(p-1)). Exact float product; not a theorem."""
    dl = deadline if deadline is not None else _deadline()
    primes = sieve_primes(prime_bound, dl)
    acc = 1.0
    for p in primes:
        _check(dl)
        if p == 2:
            continue
        acc *= 1.0 - chi4(p) / (p - 1)
    return acc


def local_root_count(p: int) -> int:
    """Number of n mod p with n^2+1 ≡ 0 (mod p)."""
    if p == 2:
        return 1  # n odd
    return 2 if p % 4 == 1 else 0


def no_covering_system(moduli: Iterable[int]) -> bool:
    """True if the listed moduli do not cover all residue classes of n
    by the local roots of n^2+1. Cheap check, not a proof of no covering.
    """
    mods = list(moduli)
    m = 1
    for q in mods:
        m *= q
    # If m is large this is expensive; caller must keep it tiny.
    if m > 20000:
        raise ValueError("covering check modulus too large")
    for n in range(m):
        blocked = False
        for q in mods:
            if (n * n + 1) % q == 0:
                blocked = True
                break
        if not blocked:
            return True
    return False


def gaussian_line_counts(re_max: int, im_max: int, deadline: float | None = None) -> dict[int, int]:
    """Count n+k i with n<=re_max, 1<=k<=im_max, n^2+k^2 prime."""
    dl = deadline if deadline is not None else _deadline()
    limit = re_max * re_max + im_max * im_max
    primes = set(sieve_primes(limit, dl))
    out = {k: 0 for k in range(1, im_max + 1)}
    for k in range(1, im_max + 1):
        for n in range(1, re_max + 1):
            _check(dl)
            if (n * n + k * k) in primes:
                out[k] += 1
    return out


def predicted_count(n_max: int, c_b: float) -> float:
    """Naive integral C_B * int_2^{n_max} dt / log(t^2+1). Simpson, not a theorem."""
    if n_max < 3:
        return 0.0
    a, b = 2.0, float(n_max)
    steps = 2000
    h = (b - a) / steps

    def f(t: float) -> float:
        return 1.0 / math.log(t * t + 1.0)

    acc = f(a) + f(b)
    for i in range(1, steps):
        x = a + i * h
        acc += 4.0 * f(x) if i % 2 else 2.0 * f(x)
    return c_b * acc * h / 3.0
