import socket


def build_payload():

    # Preamble : 3EPROTO METHOD 받음
    preamble = input() + "\n"
    method = preamble.split(" ")[1].replace("\n", "")

    # HEADER 입력받고, 공백 입력 시 페이로드 합치거나 BODY 입력 단계로 넘어감
    headers = []
    header = input()
    while header != "":
        headers.append(header)
        header = input()
    headers = "\n".join(headers) + "\n"
    bodies = ""

    # BODY 입력받고, 공백 입력 시 페이로드 합치기
    # 교환 / 교환확인 / 재교환 / 교환실패 / 메시지전송 의 경우만 BODY 필요
    if method in ['KEYXCHG', 'KEYXCHGOK', 'KEYXCHGRST', 'KEYXCHGFAIL', 'MSGSEND']:
        bodies = []
        body = input()
        while body != "":
            bodies.append(body)
            body = input()
        bodies = "\n" + "\n".join(bodies)

    # 페이로드 합체
    payload = preamble + headers + bodies

    return payload, method


def main():
    HOST = 'homework.islab.work'
    PORT = 8080

    # 연결
    while True:
        print("--------- BUILD PAYLOAD ---------")
        payload, method = build_payload()

        # CONNECT 요청 : 새 소켓 할당, 서버로부터 응답 받아옴
        if method == "CONNECT":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))

            client_socket.sendall(payload.encode("UTF-8"))
            recv = client_socket.recv(1024).decode("UTF-8")
            print(recv)
            recv_method = recv.split(" ")[1].split(("\n"))[0]

            # DENY 받을 경우, 연결 해제됨 -> 소켓 닫음
            # 새 요청 위하여 루프 재시작
            if recv_method == "DENY":
                client_socket.close()
                continue


        # DISCONNECT 요청 : 서버로부터 응답 받아옴
        elif method == "DISCONNECT":
            client_socket.sendall(payload.encode("UTF-8"))
            recv = client_socket.recv(1024).decode("UTF-8")
            print(recv)
            recv_method = recv.split(" ")[1].split(("\n"))[0]

            # BYE 받을 경우, 연결 해제됨 -> 소켓 닫음
            # 새 요청 위하여 루프 재시작
            if recv_method == "BYE":
                client_socket.close()
                continue


        # 키 교환 요청
        elif method in ['KEYXCHG', 'KEYXCHGOK', 'KEYXCHGRST', 'KEYXCHGFAIL']:
            client_socket.sendall(payload.encode("UTF-8"))

            # 처음 교환 신청하는 쪽은 : RELAYOK 를 서버로부터 받음
            # 교환 받는 쪽은 여기서 KEYXCHG를 받음
            recv = client_socket.recv(1024).decode("UTF-8")
            print(recv)
            recv_method = recv.split(" ")[1].split(("\n"))[0]


            if recv_method == 'RELAYOK':
                # 대상 클라이언트로부터 KEYXCHGOK 받음
                recv_opposite = client_socket.recv(1024).decode("UTF-8")
                print("FROM_OPPOSITE : " + recv_opposite)



        # 메시지 전송 요청
        elif method == 'MSGSEND':
            client_socket.sendall(payload.encode("UTF-8"))
            recv = client_socket.recv(1024).decode("UTF-8")
            print(recv)
            continue




if __name__ == "__main__":
    main()
