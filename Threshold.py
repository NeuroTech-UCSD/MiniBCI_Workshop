from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
import numpy as np
import time



class Threshold:
    def __init__(self) -> None:
        self.pull = False
        self.inlet = None
        self.flex_mean = 0
        self.relax_mean = 0
        self.temp_threshold = 0

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
        print("Completely relax in 3 seconds...")
        time.sleep(1)
        print("Completely relax in 2 seconds...")
        time.sleep(1)
        print("Completely relax in 1 second...")
        time.sleep(1)
        print("Completely relax now!")
        relax_data = np.array([])
        while(counter < 1000): # main loop to stream data from board
            sample, timestamp = self.inlet.pull_sample()
            print(counter, sample[0]**2)
            relax_data = np.append(relax_data,sample[0]**2)
            counter += 1
        
        mean_relax_data = np.mean(relax_data)
        print(mean_relax_data)
        
        print("STOP!!!!!!!")
        print("Clench in 3 seconds...")
        time.sleep(1)
        print("Clench in 2 seconds...")
        time.sleep(1)
        print("Clench in 1 second...")
        time.sleep(1)
        print("Clench now!")
        flex_data = np.array([])
        while(counter < 2000): # main loop to stream data from board
            sample, timestamp = self.inlet.pull_sample()
            print(counter, sample[0]**2)
            flex_data = np.append(flex_data,sample[0]**2)
            counter += 1
            
        mean_flex_data = np.mean(flex_data)
        print(mean_flex_data)
        counter = 0

        print("STOP!!!!!!!")
        

        self.relax_mean = mean_relax_data
        self.flex_mean = mean_flex_data
        self.temp_threshold = (self.relax_mean + 0.2 * (self.flex_mean - self.relax_mean))/1.5

    def listen(self):
        sample, timestamp = self.inlet.pull_sample(timeout=0.0)
        control = ""
                #check for flex
        if sample[0]**2 > self.temp_threshold:
            print("right", sample[0]**2, self.temp_threshold)
            control = "right"
                
                #else its relax
        else:
            print("left", sample[0]**2, self.temp_threshold)
            control = "left"
        return control




if __name__ == "__main__":
    threshold = Threshold()
    threshold.get_signal()
    threshold.set_pull()
    threshold.calibrate()
    threshold.listen()
