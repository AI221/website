from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return open("/home/pi/website/homepage.html","r").read()

if __name__ == '__main__':
    app.run(host='192.168.0.9',debug=True,port=80)
