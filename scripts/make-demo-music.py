import numpy as np, wave, sys
sr=44100; duration=77.167; beat=.6
out=np.zeros((int(sr*duration),2)); rng=np.random.default_rng(42)
def note(midi,start,length,vol=.12,pan=0,kind='bell'):
 n=min(int(length*sr),len(out)-int(start*sr))
 if n<=0:return
 t=np.arange(n)/sr; f=440*2**((midi-69)/12)
 if kind=='bass': y=np.sin(2*np.pi*f*t)*np.exp(-t*2)
 else: y=(np.sin(2*np.pi*f*t)+.24*np.sin(2*np.pi*f*2*t)+.08*np.sin(2*np.pi*f*3*t))*np.exp(-t*3.2)
 y*=np.minimum(t/.008,1)*np.minimum((length-t)/.08,1)*vol
 i=int(start*sr);out[i:i+n,0]+=y*(1-pan*.3);out[i:i+n,1]+=y*(1+pan*.3)
chords=[[60,64,67,71],[57,60,64,67],[53,57,60,64],[55,59,62,67]]
melodies=[[76,79,74,76],[72,76,79,76],[72,69,72,76],[74,71,67,71]]
for bar in range(32):
 start=bar*4*beat; chord=chords[(bar//2)%4]
 for k in range(8):note(chord[[0,2,1,3,2,1,3,2][k]]+12,start+k*beat/2,.9,.055,(-1)**k*.7)
 for k in [0,2]:note(chord[0]-24,start+k*beat,1.1,.11,kind='bass')
 if bar%2:
  for k,m in enumerate(melodies[(bar//2)%4]):note(m,start+k*beat,1,.075)
 for k in range(4):
  i=int((start+k*beat)*sr);n=min(int(.065*sr),len(out)-i)
  if n>0:
   t=np.arange(n)/sr;noise=rng.normal(0,1,n);noise=np.diff(noise,prepend=0)*np.exp(-t*80)*.008
   out[i:i+n]+=noise[:,None]
# Small stereo echoes and gentle fades.
for delay,gain in [(.15,.14),(.3,.07)]:
 d=int(delay*sr);out[d:]+=out[:-d,::-1]*gain
fade=np.minimum(np.arange(len(out))/sr/1.2,1)*np.minimum((len(out)-np.arange(len(out)))/sr/3,1)
out*=fade[:,None];out=np.tanh(out)*.7
with wave.open(sys.argv[1] if len(sys.argv)>1 else 'demo-music.wav','wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype('<i2').tobytes())
