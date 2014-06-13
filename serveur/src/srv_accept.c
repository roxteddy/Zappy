/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   srv_accept.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mfebvay <mfebvay@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2014/05/23 17:13:22 by mfebvay           #+#    #+#             */
/*   Updated: 2014/06/13 13:32:05 by mfebvay          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "server.h"
#include <arpa/inet.h>
#include <stdio.h>
#include <sys/socket.h>

void	srv_accept(t_data *data, int sock)
{
	struct sockaddr_in	csin;
	socklen_t			csin_len;
	int					cs;

	csin_len = sizeof(csin);
	if ((cs = accept(sock, (struct sockaddr*)&csin, &csin_len)) == -1)
		perror(data->name);
	printf("New client #%d from %s:%d\n", cs, inet_ntoa(csin.sin_addr),
			  ntohs(csin.sin_port));
	data->fds[cs].type = FD_CLIENT;
	data->fds[cs].fct_read = client_read;
	data->fds[cs].fct_write = client_write;
}