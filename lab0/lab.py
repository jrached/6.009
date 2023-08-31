# No Imports Allowed!
#Student: Juan Rached


def backwards(sound):
    #reverse the lists for both sides
    return {'rate': sound['rate'], 'left': sound['left'][::-1], 'right': sound['right'][::-1]}

def mix(sound1, sound2, p):
    #return none if rates arent equal
    if sound1['rate'] != sound2['rate']:
        return None
    else:        
        #add the each sample in each sound by respective side
        new_left = [p*x + (1-p)*y for x, y in zip(sound1['left'], sound2['left'])]
        new_right = [p*x + (1-p)*y for x, y in zip(sound1['right'], sound2['right'])]
            
        #cut it at shortest length
        cutoff = min(len(new_left), len(new_right))
        
        return {'rate': sound1['rate'],'left': new_left[0:cutoff], 'right': new_right[0:cutoff]}
    
def echo(sound, num_echos, delay, scale):
    sample_delay = round(delay*sound['rate'])
    
    left_echos = []
    right_echos = []
    old_left = sound['left'][:]
    old_right = sound['right'][:]
    
    #creates each echo and stores it in a list for each side
    for echo in range(num_echos):
        echo_left = [0 for i in range((echo + 1)*sample_delay)]
        echo_right = [0 for i in range((echo + 1)*sample_delay)]
        
        for x, y in zip(old_left, old_right):
            echo_left.append(x*scale**(echo + 1)) 
            echo_right.append(y*scale**(echo + 1)) 
            
        left_echos.append(echo_left)
        right_echos.append(echo_right)
        
    #adds each echo sample to the original sound in corresponding places
    for echo_left, echo_right in zip(left_echos, right_echos):
    
        for i in range(len(echo_left) - len(old_left)):
            old_left.append(0) 
            old_right.append(0) 
         
        new_left = [x + y for x, y in zip(old_left, echo_left)]
        new_right =  [ x + y for x, y in zip(old_right, echo_right)]
        
        old_left = new_left[:]
        old_right = new_right[:]
     
    return {'rate': sound['rate'], 'left': new_left, 'right': new_right} 


def pan(sound):
    n = len(sound['left'])
    
    #multiplies left side samples by a factor that decreases to zero 
    #and right side samples by a factor that increases to one as
    #the loop iterates through the lists
    new_left = [((n-1-i)/(n-1))*sound['left'][i] for i in range(n)] 
    new_right = [(i/(n-1))*sound['right'][i] for i in range(n)]
    
    return {'rate': sound['rate'], 'left': new_left, 'right': new_right}
    
    
    
    


def remove_vocals(sound):
    #creates a new sound composed of the difference between left and right samples
    new_sound = [sound['left'][i] - sound['right'][i] for i in range(len(sound['left']))] 
    
    return {'rate': sound['rate'], 'left': new_sound, 'right': new_sound}

# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io 
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out)) 
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav('sounds/hello.wav')
    # write_wav(backwards(hello), 'hello_reversed.wav')
    
    ##----------------SOLVE MYSTERY MESSAGE-------------------------
    # mystery = load_wav('sounds/mystery.wav')
    # solve_myst = backwards(mystery)
    # write_wav(solve_myst, 'MysterySolved.wav')


    ##----------------MIXING SOUNDS---------------------------------
    # sound1 = load_wav('sounds/synth.wav')
    # sound2 = load_wav('sounds/water.wav')
    
    # mixed = mix(sound1, sound2, 0.2)
    
    # write_wav(mixed, 'SeaSynth.wav')
    
    ##----------------TEST ECHO-------------------------------------
    # sound = load_wav('MysterySolved.wav')
    # my_echo = echo(sound, 3, 0.5, 0.5)
    # write_wav(my_echo, 'MysterySolvedEcho.wav')
    
    # sound = load_wav('sounds/chord.wav')
    # my_echo = echo(sound, 5, 0.3, 0.6)
    # write_wav(my_echo, 'chordEcho.wav')
    
    ##-----------------PAN TEST--------------------------------------
    # sound = load_wav('sounds/car.wav')
    # my_pan = pan(sound)
    # write_wav(my_pan, 'carPan.wav')
    
    ##-----------------VOCAL TEST------------------------------------
    # sound = load_wav('sounds/coffee.wav')
    # my_karaoke = remove_vocals(sound)
    # write_wav(my_karaoke, 'coffeeKaraoke.wav')
    
    
