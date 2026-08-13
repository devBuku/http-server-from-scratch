#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main()
{
  int bind_val = 0;
  int listen_val = 0;
  int ret = 0;

  int tcp_socket_fd = socket(AF_INET,     /* Domain (IPv4) */
                             SOCK_STREAM, /* Type (TCP) */
                             0            /* Protocol */
  );

  // Error Handling if file descriptor == -1

  if (tcp_socket_fd < 0)
  {
    perror("Socket error");
    return 1;
  }

  // printf("Socket creation successfull: %d\n", tcp_socket_fd);

  /*
   * Since we are creating a server we will use bind
   */

  // is a structure used to describe an IPv4 network address.
  struct sockaddr_in bind_addr;

  // clean the address structure by setting all bytes of bind_addr to 0
  memset(&bind_addr, 0, sizeof(bind_addr));

  // specify the port; htons() converts the number from the machine's byte order to network byte order.
  bind_addr.sin_port = htons(6969);

  // specify that the address is IPv4
  bind_addr.sin_family = AF_INET;

  // bind this socket to the ip address
  bind_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

  // bind socket to a port; returns -1 if error on success 0
  bind_val = bind(tcp_socket_fd, (const struct sockaddr *)&bind_addr, sizeof(bind_addr));

  if (bind_val < 0)
  {
    perror("Error in binding: bind()");
    ret = 1;
    goto exit;
  }

  // printf("Socket binding successfull: %d\n", rc);

  // listening
  listen_val = listen(tcp_socket_fd, 10);
  if (listen_val < 0)
  {
    perror("Listening failed: listen()");
    ret = 1;
    goto exit;
  }

  printf("Socket is listening on port %d....\n", ntohs(bind_addr.sin_port));

exit:
  close(tcp_socket_fd);
  return ret;
}
