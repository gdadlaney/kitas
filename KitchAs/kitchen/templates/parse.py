#additions - handle <form action = "/login">	the / is important

import sys
import pdb

def reverse_quote(quote_type):
	if(quote_type == '"'):
		return "'"
	else:
		return '"'



filename = sys.argv[1]

read_fd = open(filename, "r")
write_fd = open("1"+filename, "w")

check_string_start = ['href=', 'src=', 'url(']
load_staticfiles_flag = 0

for line in read_fd:
	#pdb.set_trace()
	if "{% load staticfiles %}" in line:
		load_staticfiles_flag = 1

	if ("<!DOCTYPE html>" in line) and load_staticfiles_flag == 0:
		write_fd.write("{% load staticfiles %}\n")
		write_fd.write(line)
		continue

	check_string_flag = 0
	partitioned_line = line
	new_line = ""
	for ch_str in check_string_start:
		if(ch_str in partitioned_line):
			check_string_flag = 1

			new_line_part = ""
			while partitioned_line.count(ch_str) > 0:
				#pdb.set_trace()
				temp = partitioned_line.partition(ch_str)
				if ('{%' in temp[2] and '%}' in temp[2]):
					temp2 = temp[2].partition('%}')
					new_line_part += temp[0] + temp[1] + temp2[0] + temp2[1]
					partitioned_line = temp2[2]
				else:
					#pdb.set_trace()
					quote_type = temp[2][0]		#finding out if ' or " is used in href=''
					rev_quote_type = reverse_quote(quote_type)
					temp = partitioned_line.partition(ch_str + quote_type)	#searching fo the next quote

					temp2 = temp[2].partition(quote_type)

					if ("http" in temp2[0] or '#' in temp2[0] or "#" in temp2[0] or 'google' in temp2[0]):
						new_line_part += temp[0] + temp[1] + temp2[0] + temp2[1]
					else:
						if (temp2[0][0] == "/"):
							new_line_part += temp[0] + temp[1] + temp2[0] + temp2[1]
						elif ('.' in temp2[0] and not ".html" in temp2[0]):
							new_line_part += temp[0] + temp[1] + "{% static "+rev_quote_type + temp2[0] + rev_quote_type+" %}" + temp2[1]
						elif (".html" in temp2[0]):
							temp3 = temp2[0].partition('.html')
							new_line_part += temp[0] + temp[1] + "/" + temp3[0] + temp3[2] + temp2[1]
						else:
							new_line_part += temp[0] + temp[1] + "/" + temp2[0] + temp2[1]
					partitioned_line = temp2[2]

			new_line += new_line_part

	if check_string_flag == 1:
		new_line += partitioned_line
		write_fd.write(new_line)
	else:
		write_fd.write(line)
		continue

read_fd.close()
write_fd.close()