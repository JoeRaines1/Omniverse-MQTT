import omni
import omni.ui as ui
from pxr import Usd
import random

omni.kit.pipapi.install(package="paho-mqtt", version="1.6.1", module="paho.mqtt")
from paho.mqtt import client as mqtt_client

class MqttSceneControlllerExtension(omni.ext.IExt):
    topic = "mqtt_scene_controll"
    
    # Runs the following code when the extension starts
    def on_startup(self, ext_id):

        self.stage = omni.usd.get_context().get_stage()
        self.toggle_lights = False
        self.toggle_curtains = False
        # Everytime an Omniverse update event occurs on_app_update_event in called
        self._app_update_sub = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(
            self._on_app_update_event)

        def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    # Client subscribes to the MQTT topic
                    client.subscribe(self.topic)      
        
        def on_message(client, userdata, msg):
            # Decodes and stores the MQTT message
            message = msg.payload.decode()
            if 'lights' in message:
                # Determines if the current light status needs to be changed
                self.toggle_lights = True
                
            elif 'curtains' in message:
                # Determines if the current curtain status needs to be changed
                self.toggle_curtains = True

        # Creates an MQTT client
        self.client = mqtt_client.Client(f"python-mqtt-{random.randint(0, 1000)}")
        self.client.user_data_set(self)
        # Calls on_connect when first connecting to the MQTT broker
        self.client.on_connect = on_connect
        # Calls on_message everytime a message is recieved
        self.client.on_message = on_message
        # Connects the MQTT clien to the provide url and port
        self.client.connect("test.mosquitto.org", 1883)
        self.client.loop_start()

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            def controll_lights():
                payload = 'lights'
                # Uses the broker site to send the payload as a message
                self.client.publish(self.topic, payload.encode("utf-8"))
                
            def controll_curtains():
                payload = "curtains"
                # Uses the broker site to send the payload as a message
                self.client.publish(self.topic, payload.encode("utf-8"))

            with ui.HStack():
                # Calls controll_lights whenever the lights button is clicked
                ui.Button("Lights", clicked_fn=controll_lights)
                # Calls controll_curtains whenever the curtains button is clicked
                ui.Button("Curtains", clicked_fn=controll_curtains)
    
    # Called when the extension is being shutdown
    def on_shutdown(self):
        # Disconnects the client from any brokers that it connected to
        self.client.disconnect()
    
    def _on_app_update_event(self, evt):
        # The path to the assets in the scene whose visibilty is being changed
        curtains = ["/World/Done_Set/Outer_Sink_GRP/Extended_Curtains", 
                "/World/Done_Set/Base_Structure/Curtain_GRP/Curtain_Extended", 
                "/World/Done_Set/Base_Structure/Curtain_GRP1/Curtains_Down"]
        lights = ["/World/CylinderLight", "/World/RectLight", "/World/RectLight_01",
            "/World/RectLight_02", "/World/RectLight_03"]
        
        # Determines if the curtains visibility should be changed
        if self.toggle_curtains:
            # Changes the visibility of the provided objects
            omni.kit.commands.execute('ToggleVisibilitySelectedPrims', selected_paths = curtains, stage= self.stage)
            self.toggle_curtains = False

        # Determines if the lights visibility should be changed
        if self.toggle_lights:
            # Changes the visibility of the provided objects
            omni.kit.commands.execute('ToggleVisibilitySelectedPrims', selected_paths = lights, stage= self.stage)
            self.toggle_lights = False# 