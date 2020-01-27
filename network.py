import numpy as np


def generate_random_durations(min_time=40):
    return int(np.random.exponential(50.0) + min_time)


class Network:
    def __init__(self, segment_size, segment_time, buffer_capacity, states, video_length):
        self.video_length = video_length
        self.segment_size = segment_size
        self.rest = 0
        self.segment_time = segment_time
        self.capacity = buffer_capacity

        self.tab_of_time = []
        self.tab_of_values = []
        self.tab_of_time.append(0.0)
        self.tab_of_values.append(0.0)

        self.states = states
        self.current_state = states[0]

        self.segments_to_download = int(video_length/segment_time)
        if video_length % segment_time != 0:
            self.segments_to_download += 1

        self.tab_of_states_values = []
        self.tab_of_states_times = []
        self.tab_of_states_values.append(self.current_state)
        self.tab_of_states_times.append(0.0)
        self.tab_of_states_values.append(self.current_state)
        self.tab_of_states_times.append(generate_random_durations(40) - 0.001)
        self.change_state()
        self.tab_of_states_times.append(self.tab_of_states_times[1]+0.001)
        self.tab_of_states_values.append(self.current_state)
        self.change_state()

    def change_state(self):
        if self.current_state == self.states[0]:
            self.current_state = self.states[1]
        else:
            self.current_state = self.states[0]

    def make_a_simulation(self):
        while self.segments_to_download > 0:
            curr_segment = self.segment_size - self.rest
            self.rest = 0.0
            time = curr_segment/self.current_state
            t = self.tab_of_time[-1] + time
            if t < self.tab_of_states_times[-1]:
                if self.tab_of_values[-1] - time + self.segment_time <= 30:
                    if self.tab_of_values[-1] - time >= 0:
                        self.tab_of_time.append(t - 0.001)
                        self.tab_of_time.append(t)
                        self.tab_of_values.append(self.tab_of_values[-1] - time)
                        self.tab_of_values.append(self.tab_of_values[-1] + self.segment_time)
                    else:
                        self.tab_of_time.append(self.tab_of_time[-1] + self.tab_of_values[-1])
                        self.tab_of_values.append(0)
                        self.tab_of_time.append(t - 0.001)
                        self.tab_of_values.append(0)
                        self.tab_of_time.append(t)
                        self.tab_of_values.append(self.tab_of_values[-1] + self.segment_time)
                    self.segments_to_download -= 1
                else:
                    self.tab_of_time.append(t)
                    self.tab_of_values.append(self.tab_of_values[-1] - time)
            elif t == self.tab_of_states_times[-1]:
                if self.tab_of_values[-1] - time + self.segment_time <= 30:
                    self.change_state()
                    if self.tab_of_values[-1] - time >= 0:
                        self.tab_of_time.append(t - 0.001)
                        self.tab_of_time.append(t)
                        self.tab_of_values.append(self.tab_of_values[-1] - time)
                        self.tab_of_values.append(self.tab_of_values[-1] + self.segment_time)
                    else:
                        self.tab_of_time.append(self.tab_of_time[-1] + self.tab_of_values[-1])
                        self.tab_of_values.append(0)
                        self.tab_of_time.append(t - 0.001)
                        self.tab_of_values.append(0)
                        self.tab_of_time.append(t)
                        self.tab_of_values.append(self.tab_of_values[-1] + self.segment_time)
                    self.tab_of_states_times.append(self.tab_of_states_times[-1] + generate_random_durations() - 0.001)
                    self.tab_of_states_times.append(self.tab_of_states_times[-1] + 0.001)
                    self.tab_of_states_values.append(self.current_state)
                    self.change_state()
                    self.tab_of_states_values.append(self.current_state)
                    self.change_state()
                    self.segments_to_download -= 1
                else:
                    self.tab_of_time.append(t)
                    self.tab_of_values.append(self.tab_of_values[-1] - time)
            else:
                self.rest = (self.tab_of_states_times[-1] - self.tab_of_time[-1])*self.current_state
                self.change_state()
                if self.tab_of_values[-1] - (self.tab_of_states_times[-1]-self.tab_of_time[-1]) >= 0:
                    self.tab_of_values.append(self.tab_of_values[-1] -
                                              (self.tab_of_states_times[-1]-self.tab_of_time[-1]))
                    self.tab_of_time.append(self.tab_of_states_times[-1])
                else:
                    self.tab_of_time.append(self.tab_of_time[-1]+self.tab_of_values[-1])
                    self.tab_of_values.append(0)
                    self.tab_of_time.append(self.tab_of_states_times[-1])
                    self.tab_of_values.append(0)
                self.tab_of_states_times.append(self.tab_of_states_times[-1] + generate_random_durations() - 0.001)
                self.tab_of_states_times.append(self.tab_of_states_times[-1] + 0.001)
                self.tab_of_states_values.append(self.current_state)
                self.change_state()
                self.tab_of_states_values.append(self.current_state)
                self.change_state()
        if self.tab_of_time[-1]+self.tab_of_values[-1] > self.tab_of_states_times[-1]:
            self.tab_of_time.append(self.tab_of_time[-1]+self.tab_of_values[-1])
            self.tab_of_values.append(0)
            self.tab_of_states_times.append(self.tab_of_time[-1])
            self.tab_of_states_values.append(self.current_state)
        elif self.tab_of_time[-1]+self.tab_of_values[-1] == self.tab_of_states_times[-1]:
            self.tab_of_time.append(self.tab_of_time[-1]+self.tab_of_values[-1])
            self.tab_of_values.append(0)
        else:
            self.tab_of_time.append(self.tab_of_time[-1]+self.tab_of_values[-1])
            self.tab_of_values.append(0)
            self.tab_of_states_times.pop()
            self.tab_of_states_times.pop()
            self.tab_of_states_values.pop()
            self.tab_of_states_times.append(self.tab_of_time[-1])
