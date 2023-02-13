from pyempatica import EmpaticaClient, EmpaticaE4, EmpaticaDataStreams, EmpaticaServerConnectError
import time

class E4:
    def __init__(self):
        try:
            self.client = EmpaticaClient()
            print("Connected to E4 Streaming Server...")
            self.client.list_connected_devices()
            print("Listing E4 devices...")

        except EmpaticaServerConnectError:
            print("Failed to connect to server, check that the E4 Streaming Server is open and connected to the BLE dongle.")

        self._recording = False

    def ready(self):
        self.e4 = EmpaticaE4(self.client.device_list[0])
        if self.e4.connected:
            print("Connected to", str(self.client.device_list[0]), "device...")

            for stream in EmpaticaDataStreams.ALL_STREAMS:
                self.e4.subscribe_to_stream(stream)
            print("Subscribed to E4 streams")

        else:
            print("Could not connect to Empatica E4:", self.client.device_list[0])

    def stream(self):
        self.e4.start_streaming()
        print("Start E4 Streaming")
        while True:
            pass

    def record(self, save_path):
        if not self._recording:
            self._recording = True

            self.e4.clear_readings()

    def stop_record(self):
        if self._recording:
            self._recording = False

            self.e4.suspend_streaming()

    def save_data(self, save_path):
        if self._recording:
            self._recording = False

        self.e4.save_readings(save_path + "/e4.txt")
        self.e4.start_streaming()

    def terminate(self):
        self.e4.disconnect()
        self.e4.close()

        self.client.close()

    def clear(self):
        self.e4.clear_readings()
        print("Cleaning up connections...")