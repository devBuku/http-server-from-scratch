#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdbool.h>

int handle_client(int client_socket_fd)
{
  ssize_t n = 0;
  char buffer[1024];
  char *hello = "HTTP/1.0 200 OK\r\n\r\n<h1>Hello, World!</h1>";

  printf("\n----\n");

  while (1)
  {
    memset(buffer, 0, sizeof(buffer));

    n = read(client_socket_fd, buffer, sizeof(buffer) - 1);

    if (n < 0)
    {
      perror("read(client)");
      return -1;
    }
    else if (n == 0)
    {
      printf("Connection closed gracefully!!!\n");
      break;
    }

    printf("Request:\n%s", buffer);

    (void)write(client_socket_fd, hello, strlen(hello));

    close(client_socket_fd);

    break;
  }
  printf("\n----\n");

  return 0;
}

int main()
{
  int bind_val = 0;
  int listen_val = 0;
  int ret = 0;
  int enabled = true;

  // is a structure used to describe an IPv4 network address.
  struct sockaddr_in bind_addr;

  int tcp_socket_fd = 0;
  int client_socket_fd = 0;

  // clean the address structure by setting all bytes of bind_addr to 0
  memset(&bind_addr, 0, sizeof(bind_addr));

  tcp_socket_fd = socket(AF_INET,     /* Domain (IPv4) */
                         SOCK_STREAM, /* Type (TCP) */
                         0            /* Protocol */
  );

  // Error Handling if file descriptor == -1

  if (tcp_socket_fd < 0)
  {
    perror("Socket error");
    return 1;
  }

  (void)setsockopt(tcp_socket_fd, SOL_SOCKET, SO_REUSEADDR, &enabled, sizeof(enabled)); // TODO: what is this doing (on a high level it is telling to reuse the socket but what are those variable)

  // printf("Socket creation successfull: %d\n", tcp_socket_fd);

  /*
   * Since we are creating a server we will use bind
   */

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

  while (1)
  {

    printf("Server is listening on port %d....\n", ntohs(bind_addr.sin_port));

    client_socket_fd = accept(tcp_socket_fd, NULL, NULL);

    if (client_socket_fd < 0)
    {
      perror("accept()");
      continue;
    }

    printf("Got a connection.\n");

    if (handle_client(client_socket_fd) < 0)
    {
      ret = 1;
      goto exit;
    }
  }

exit:
  close(tcp_socket_fd);
  return ret;
}
