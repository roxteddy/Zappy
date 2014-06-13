/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mfebvay <mfebvay@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2014/06/04 07:07:28 by mfebvay           #+#    #+#             */
/*   Updated: 2014/06/13 14:52:12 by mfebvay          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "server.h"
#include <stdlib.h>

int		main(int ac, char **av)
{
	t_data	data;

	(void)ac;
	init_data(&data, av);
	init_server(&data);
	while("loop")
	{
		init_fd(&data);
		data.sel = select(data.fd_nb + 1, &data.fd_read, &data.fd_write,
						  NULL, &data.timeout);
		check_fd(&data);
	}
	return (0);
}
