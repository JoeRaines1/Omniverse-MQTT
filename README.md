This code uses MQTT to control objects in a scene.
The extension creates a GUI with 2 buttons and when either of the buttons is clicked the broker service is used to send a message to every device that is subscribed to the provided topic, the Omniverse scene subscribes to the topic on startup.
Once Omniverse receives the message it determines if the visibility of the lights or curtains is supposed to be changed and then changes it. 
This project was simply a proof of concept to show that Omniverse can be used to both send and recieve MQTT messages. The code writen to create and control the extension are here: 
Video of the code working:

https://github.com/JoeRaines1/Omniverse-MQTT/assets/153453434/3934d57c-08ee-4ad4-be9e-230d71f30f0a

