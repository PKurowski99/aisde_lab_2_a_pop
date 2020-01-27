from matplotlib import pyplot as plt
from matplotlib import ticker
from network import Network

VIDEO_DURATION = 300.0
SEGMENT_SIZE = 20.0
SEGMENT_TIME = 2.0
BUFFER_CAPACITY = 30.0
TAB_OF_TIME = []
TAB_OF_VALUES = []
TAB_OF_STATES_TIME = []
TAB_OF_STATES_VALUES = []
STATES = [20.0, 2.0]

network = Network(SEGMENT_SIZE, SEGMENT_TIME, BUFFER_CAPACITY, STATES, VIDEO_DURATION)
network.make_a_simulation()

plt.switch_backend('TkAgg')
plt.subplots_adjust(hspace=0)
ax1 = plt.subplot(211)
plt.title("Stan bufora w zaleznosci od czasu")
ax1.set_xlim(0, network.tab_of_time[len(network.tab_of_time) - 1])
ax1.grid(axis='both', which='both')
ax1.yaxis.set_major_locator(ticker.AutoLocator())
ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax1.xaxis.set_major_locator(ticker.AutoLocator())
ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
color = '#00871F'
ax1.set_ylim(top=21)
ax1.set_ylabel("Pasmo [Mbps]", color=color)
ax1.set_xlabel("Czas [s]")
ax1.tick_params(axis='y', labelcolor=color)
ax1.plot(network.tab_of_states_times, network.tab_of_states_values, color=color, drawstyle='steps-post')

color = '#990763'
ax2 = ax1.twinx()
ax2.set_xlabel("Czas symulacji [s]")
ax2.set_ylabel("Bufor [s]", color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.plot(network.tab_of_time, network.tab_of_values, color=color, lw=0.75)
plt.show()
