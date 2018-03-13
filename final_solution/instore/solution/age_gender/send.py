import time
import cv2
from kafka import KafkaProducer
#Initialising Kafka Producer, cluster IP :192.168.3.174, topic: video
producer = KafkaProducer(bootstrap_servers='Extrack.bridgei2i.in:9092')
topic = 'age'

def video_emitter(video):
    video = cv2.VideoCapture(video)
    print(' emitting.....')
    #get image matrix
    while True: 
        success, image = video.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #convert image matrix to ndarray
        ret,jpeg = cv2.imencode('.png', gray)
        
        #convert ndarray into bytes and sending to kafka server
        producer.send(topic, jpeg.tobytes())
    video.release()
    print('done emitting')

if __name__ == '__main__':
    video_emitter('test.mp4')

