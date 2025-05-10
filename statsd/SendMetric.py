import socket

def send_udp_message(message, ip='1.1.1.1', port=8125):
    # 创建一个 UDP socket 对象
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 发送数据到指定的 IP 和端口
        sock.sendto(message.encode('utf-8'), (ip, port))
        print(f"Message sent to {ip}:{port}")
    finally:
        # 关闭 socket
        sock.close()

# 使用该函数发送消息


if __name__ == "__main__":
    send_udp_message("Hello, World!")
    