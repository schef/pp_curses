#!/usr/bin/python3
import pool
import practices
import tones
myprac = practices.Practices()
mypool = pool.tonesPool(toneFilter=["white"])
myprac.setRandom2SepBy1FromPool(mypool.pool)
