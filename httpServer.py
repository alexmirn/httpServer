# GET /index.html HTTP/1.1
# GET /index.zzz HTTP/1.1
# GET /sudo.html HTTP/1.1
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
# import os
import time

class HttpServer(object):
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.http_conf = None
        self.file_name = None
        self.inData_words = None


    def start(self):
        self.http_conf = self.parse('http.conf')
        self.sock.bind((self.http_conf.get('address'), int(self.http_conf.get('port'))))
        self.sock.listen(2)

        print('server started work at address ' + self.http_conf.get('address'))
        print('port ' + self.http_conf.get('port'))
        
        conn, addr = self.sock.accept()
        print 'connected:', addr

        while True:
            inData = conn.recv(10000)
            print(inData)
            self.inData_words = inData.split()

            # if not self.inData_words:
            #     conn.send('\r\n')
            # elif self.inData_words[0] == 'GET':
            if self.inData_words[0] == 'GET':
                if len(self.inData_words) >= 3:
                    http_version = self.inData_words[2]
                    if http_version != 'HTTP/1.1' and http_version != 'HTTP/1.0' and http_version != 'HTTP/0.9':
                        conn.send(self.response(405))
                    else:
                        conn.send(self.do_GET())
                else:
                    conn.send(self.response(405))
            else:
                inData = inData.decode('utf-8', 'ignore')
                if inData == '':
                    break
                conn.send(self.response(405))

    def response(self, id):
        if id == 405:
            return "405 Method Not Allowed\r\n"
        if id == 404:
            return '404 ' + self.http_conf.get('root_dir') + self.file_name + ' Not Found: \n'
        if id == 200:
            return self.inData_words[2] + ' 200 OK\n'

    def do_GET(self):
        try:
            file_name = self.inData_words[1].rsplit('/',1)[1]
            self.file_name = file_name
            file_extension = file_name.rsplit('.',1)[1]
        except IndexError:
            return self.response(404)

        try:
            with open(self.http_conf.get('root_dir') + file_name) as f:
                header = self.response(200) + \
                'Connection: close\nContent-Length: {}\nContent-Type: {}\nDate: %{}\n\n'\
                .format(str(len(f.read())), self.mime_type(file_extension), str(time.strftime("%c")))

                f.seek(0)
                send_Data = header + f.read() + '\n\n'
                return send_Data
        except IOError:
                return self.response(404)

    def parse(self, file_name):
        with open(file_name) as f:
            new_dict = dict()

            while True:
                file_line = f.readline()
                if not file_line:
                    return new_dict
                    break
                file_line.split()
                file_line_words = file_line.split()
                try:
                    new_dict.update({file_line_words[0]: file_line_words[1]}) 
                except IndexError:
                    pass

    def mime_type(self, file_extension):
        mime = self.parse('mime.types')
        if mime.has_key(file_extension):
            return mime.get(file_extension)
        return 'application/octet-stream'

if __name__ == '__main__':
    sock1 = HttpServer()
    
    sock1.start()



# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import socket
# # import os
# import time

# class HttpServer(object):
#     def __init__(self):
#         self.sock = socket.socket()
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#     def parse(self, file_name):
#         with open(file_name) as f:
#             new_dict = dict()

#             while True:
#                 file_line = f.readline()
#                 if not file_line:
#                     return new_dict
#                     break
#                 file_line.split()
#                 file_line_words = file_line.split()
#                 try:
#                     new_dict.update({file_line_words[0]: file_line_words[1]}) 
#                 except IndexError:
#                     pass

#     def start(self):
#         http_conf = self.parse('http.conf')
#         self.sock.bind((http_conf.get('address'), int(http_conf.get('port'))))
#         self.sock.listen(2)

#         print('server started work at address ' + http_conf.get('address'))
#         print('port ' + http_conf.get('port'))
        
#         conn, addr = self.sock.accept()
#         print 'connected:', addr
#         while True:
#             try:
#                 inData = conn.recv(100000000)
#                 if inData == '\r\n':
#                     conn.send('\r\n')
#                 else:
#                     inData_words = inData.split()
#                     if not inData_words:
#                         pass
#                     elif inData_words[0] == 'GET':
#                         if len(inData_words) >= 3:
#                             http_version = inData_words[2]
#                             if http_version != 'HTTP/1.1' and http_version != 'HTTP/1.0' and http_version != 'HTTP/0.9':
#                                 conn.send("405 Method Not Allowed\r\n")
#                             else:
#                                 send_Data = self.do_GET(http_conf, inData_words)
#                                 conn.send(send_Data + '\n')
#                         else:
#                             conn.send("405 Method Not Allowed\r\n")
#                     else:
#                         inData = inData.decode('utf-8', 'ignore')
#                         if inData == '':
#                             break
#                         conn.send("405 Method Not Allowed\r\n")
#             except KeyboardInterrupt:
#                 print("KeyboardInterrupt!!!")
#                 break

#     def do_GET(self, http_conf, inData_words):
#         mime = self.parse('mime.types')
#         try:
#             file_name = inData_words[1].rsplit('/',1)[1]
#             file_extension = file_name.rsplit('.',1)[1]
#         except IndexError:
#             return '404 ' + http_conf.get('root_dir') + inData_words[1] + ' Not Found: \n'

#         if mime.has_key(file_extension):
#             file_extension_exist = mime.get(file_extension)
#         else:
#             file_extension_exist = 'application/octet-stream'

#         try:
#             with open(http_conf.get('root_dir') + file_name) as f:
#                 header = '%s 200 OK\nConnection: close\nContent-Length: %s\nContent-Type: %s\nDate: %s\n\n' \
#                 % (inData_words[2], str(len(f.read())), file_extension_exist, str(time.strftime("%c")))
#                 f.seek(0)
#                 send_Data = header + f.read()
#                 f.close()
#                 return send_Data
#         except IOError:
#                 send_Data = '404 ' + http_conf.get('root_dir') + file_name + ' Not Found: \n'
#                 return send_Data

# if __name__ == '__main__':
#     sock1 = HttpServer()
    
#     sock1.start()















        # while True:
        #     inData = conn.recv(100000000)
        #     if inData == '\r\n':
        #         conn.send('\r\n')
        #     else:
        #         inData_words = inData.split()
        #         if not inData_words:
        #             pass
        #         elif inData_words[0] == 'GET':
        #             if len(inData_words) >= 3:
        #                 http_version = inData_words[2]
        #                 if http_version != 'HTTP/1.1' and http_version != 'HTTP/1.0' and http_version != 'HTTP/0.9':
        #                     conn.send(self.response(405))
        #                 else:
        #                     send_Data = self.do_GET(http_conf, inData_words)
        #                     conn.send(send_Data + '\n')
        #             else:
        #                 conn.send(self.response(405))
        #         else:
        #             inData = inData.decode('utf-8', 'ignore')
        #             if inData == '':
        #                 break
        #             conn.send(self.response(405))