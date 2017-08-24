def prime_factors(n):
  if n<0:
    n = -n
  if n<2:
    return []
  facts = []
  m = n
  for i in xrange(2, int(n/2)+1):
    # because i is monotonically increasing, we know that all new i's that
    # divide m are prime, because if they weren't, then we'd already have found
    # a factor at a previous i.
    while m%i==0:
      facts.append(i)
      m/=i
    if m==1:
      return facts
  # if we got here, n was prime
  facts.append(n)
  return facts
