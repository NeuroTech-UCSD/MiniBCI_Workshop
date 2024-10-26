from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
import numpy as np
import time
#comment

class Threshold:
    def __init__(self) -> None:
        self.pull = False
        self.inlet = None
        self.flex_mean = 0
        self.relax_mean = 0
    
    def get_signal(self):
        streams = resolve_stream('type', 'EEG')
        for stream in streams:
            if stream.name() == "Siya":
                self.inlet = StreamInlet(stream)
                break
    
    def set_pull(self):
        self.pull = True

    def calibrate(self):
        counter = 0
        print("Calibrating starting...")
        time.sleep(2)
        print("Clench in 3 seconds...")
        time.sleep(1)
        print("Clench in 2 seconds...")
        time.sleep(1)
        print("Clench in 1 second...")
        time.sleep(1)
        print("Clench now!")
        flex_data = np.array([])
        while(counter < 1000): # main loop to stream data from board
            print(counter)
            sample, timestamp = self.inlet.pull_sample()
            flex_data = np.append(flex_data,sample[0]**2)
            counter += 1

        
            
        mean_flex_data = np.mean(flex_data)
        print(mean_flex_data)
        counter = 0

        print("STOP!!!!!!!")
        time.sleep(2)
        print("Completely relax in 3 seconds...")
        time.sleep(1)
        print("Completely relax in 2 seconds...")
        time.sleep(1)
        print("Completely relax in 1 second...")
        time.sleep(1)
        print("Completely relax now!")
        relax_data = np.array([])
        while(counter < 2000): # main loop to stream data from board
            print(counter)
            sample, timestamp = self.inlet.pull_sample()
            relax_data = np.append(relax_data,sample[0]**2)
            counter += 1
        
        mean_relax_data = np.mean(relax_data)
        print(mean_relax_data)

        self.relax_mean = mean_relax_data
        self.flex_mean = mean_flex_data

    def listen(self):
        while self.pull == True:
            sample, timestamp = self.inlet.pull_sample()
            if sample[0]**2 > self.relax_mean + 0.2 * (self.flex_mean - self.relax_mean):
                print("Siya is Flexing")
            else:
                print("No Flex")


if __name__ == "__main__":
    threshold = Threshold()
    threshold.get_signal()
    threshold.set_pull()
    threshold.calibrate()
    threshold.listen()
