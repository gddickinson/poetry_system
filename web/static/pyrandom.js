// Python's `random` module (CPython 3.x MT19937) in JavaScript, so the browser generator makes the same poem as
// `random.seed(n)` + PoetryGenerator in Python. Implements seed(int), random(), getrandbits(k<=32), _randbelow,
// randint, choice and sample exactly as CPython does for the cases the generator uses.

const N = 624, M = 397;

export class PyRandom {
  constructor(seed = 0) { this.mt = new Uint32Array(N); this.mti = N + 1; this.seed(seed); }

  initGenrand(s) {
    const mt = this.mt;
    mt[0] = s >>> 0;
    for (let i = 1; i < N; i++) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = (Math.imul(1812433253, prev) + i) >>> 0;
    }
    this.mti = N;
  }

  initByArray(key) {
    const mt = this.mt;
    this.initGenrand(19650218);
    let i = 1, j = 0;
    for (let k = Math.max(N, key.length); k; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(prev, 1664525)) + key[j] + j) >>> 0;
      i++; j++;
      if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
      if (j >= key.length) j = 0;
    }
    for (let k = N - 1; k; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(prev, 1566083941)) - i) >>> 0;
      i++;
      if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
    }
    mt[0] = 0x80000000;
  }

  // random.seed(n) for a non-negative or negative integer n (abs value split into 32-bit words, little-endian).
  seed(n) {
    let v = BigInt(Math.abs(Math.trunc(Number(n))));
    const key = [];
    if (v === 0n) key.push(0);
    while (v > 0n) { key.push(Number(v & 0xffffffffn)); v >>= 32n; }
    this.initByArray(key);
  }

  genrandUint32() {
    const mt = this.mt;
    if (this.mti >= N) {
      let kk = 0, y;
      for (; kk < N - M; kk++) {
        y = (mt[kk] & 0x80000000) | (mt[kk + 1] & 0x7fffffff);
        mt[kk] = mt[kk + M] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0);
      }
      for (; kk < N - 1; kk++) {
        y = (mt[kk] & 0x80000000) | (mt[kk + 1] & 0x7fffffff);
        mt[kk] = mt[kk + (M - N)] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0);
      }
      y = (mt[N - 1] & 0x80000000) | (mt[0] & 0x7fffffff);
      mt[N - 1] = mt[M - 1] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0);
      this.mti = 0;
    }
    let y = mt[this.mti++];
    y ^= y >>> 11;
    y = (y ^ ((y << 7) & 0x9d2c5680)) >>> 0;
    y = (y ^ ((y << 15) & 0xefc60000)) >>> 0;
    y ^= y >>> 18;
    return y >>> 0;
  }

  random() {
    const a = this.genrandUint32() >>> 5, b = this.genrandUint32() >>> 6;
    return (a * 67108864 + b) / 9007199254740992;
  }

  getrandbits(k) {
    if (k <= 0 || k > 32) throw new Error('getrandbits: 1..32 bits only');
    return this.genrandUint32() >>> (32 - k);
  }

  randbelow(n) {
    const k = 32 - Math.clz32(n);  // n.bit_length() for 0 < n < 2**32
    let r = this.getrandbits(k);
    while (r >= n) r = this.getrandbits(k);
    return r;
  }

  randint(a, b) { return a + this.randbelow(b - a + 1); }

  choice(seq) {
    if (!seq.length) throw new IndexError('Cannot choose from an empty sequence');
    return seq[this.randbelow(seq.length)];
  }

  // random.sample for populations of at most 21 items (CPython's pool branch).
  sample(population, k) {
    const n = population.length;
    if (k < 0 || k > n) throw new Error('Sample larger than population or is negative');
    if (n > 21) throw new Error('sample: only small populations are ported');
    const pool = population.slice(), result = new Array(k);
    for (let i = 0; i < k; i++) {
      const j = this.randbelow(n - i);
      result[i] = pool[j];
      pool[j] = pool[n - i - 1];
    }
    return result;
  }
}

// Python's IndexError, so ported `except IndexError` blocks can catch exactly what Python catches.
export class IndexError extends Error {}
