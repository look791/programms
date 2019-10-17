
from wit import Wit

client = Wit('ZF464AV6N4XA4O2W7GKK5RA5ROGMYCLO')

resp = None
i = 0
err = 0
well = 0

with open('probe_3.wav', 'rb') as f:
  resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
  print(str(resp['_text']))

  ref_long = ('i know the human being and fish can coexist peacefully')
  print(ref_long)
  ref = ('i', 'know', 'the', 'human', 'being', 'and', 'fish', 'can', 'coexist', 'peacefully')
  #print(ref)
  #print("\n")
while(i != 10):
  a = str(resp['_text']).find(ref[i])
  if (a == -1):
    err = err + 1
  else:
    well = well + 1
  i = i + 1
result = (len(ref) - err) * 10
print(f'Result matched with reference in: {result}%')


