from PIL import Image, ImageDraw
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

host = "localhost"
port = 8080

class picServer(BaseHTTPRequestHandler):
    def do_GET(self):
        
        query = urlparse(self.path).query
        if query:
            q = dict(qc.split("=") for qc in query.split("&"))
            print("here") 
            if "r" in q and "g" in q and "b" in q:
                r, g, b = int(q["r"]), int(q["g"]), int(q["b"])
                if r in range(0, 256) and g in range(0, 256) and b in range(0, 256):
                    filename = genImage(r, g, b)
                                       
                    self.send_response(200)
                    self.send_header("Content-type", "image/png")
                    self.end_headers()

                    self.wfile.write(loadImage(filename))
                    return 
        else:
            print("AAAA")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>:)</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Oops</p>", "utf-8"))
            self.wfile.write(bytes("</html>", "utf-8"))

def genImage(r, g, b):
    color = (r, g, b)
    img = Image.new("RGBA", (30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 20, 20), fill=color, outline=color)
    filename = "{}_{}_{}.png".format(r, g, b)
    img.save(filename, "PNG")
    return filename

def loadImage(filename):
    with open(filename, "rb") as f:
        return f.read()

if __name__ == "__main__":
    serv = HTTPServer((host, port), picServer)

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass

    serv.server_close()
