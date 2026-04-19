# Exercise description

Please write a command-line tool to analyze the content of log files. The tool should accept the log file location(s) and operation(s) as input arguments and return the results of the operations as output. The tool should be packaged according to the latest PEP packaging standards.

## Requirements

- Python >= 3.11
- A functioning and standalone cli is the minimum requirement, however you can enhance your
project according to DevSecOps best practices. The more mature your solution is the better.
- The tool should be as fault tolerant as possible and also should be built with future extensibility
in mind. Consider different input or output formats.
- Please also create a Dockerfile in your solution with the application as its entry point and include
instructions on how to run it as a container/service

## Program arguments

- Arguments:
  - input: Path to one or more input files.
  - output: Path to a file to save output in plain text JSON format.
- Options:
  - --mfip: most frequent IP
  - --lfip: least frequent IP
  - --eps: events per second
  - --bytes: total amount of bytes exchanged

## Sample data

As sample input file, please use the Squid Proxy access logs from the following URL1:

<https://www.secrepo.com/squid/access.log.gz>

The data is in CSV format with 10 fields. After the second field they are separated by a space:

`1157689324.156 1372 10.105.21.199 TCP_MISS/200 399 GET http://www[.]google-analytics[.]com/__utm.gif? badeyek DIRECT/66.102.9.147 image/gif`

which, after proper parsing should be split as follow:

Field 1: 1157689324.156 [Timestamp in seconds since the epoch]
Field 2: 1372 [Response header size in bytes]
Field 3: 10.105.21.199 [Client IP address]
Field 4: TCP_MISS/200 [HTTP response code]
Field 5: 399 [Response size in bytes]
Field 6: GET [HTTP request method]
Field 7: <http://www.google-analytics.com/__utm.gif?> [URL]
Field 8: badeyek [Username]
Field 9: DIRECT/66.102.9.147 [Type of access/destination IP address]
Field 10: image/gif [Response type]

## Assignment delivery

Please send us a link to a public repository of your choice containing your assignment project. If questions arise during development, please make assumptions and document it in the code or in the readme.
