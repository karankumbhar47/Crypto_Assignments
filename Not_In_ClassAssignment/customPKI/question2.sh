crtPath=$1

# We used following command to get following output 
openssl x509 -in $crtPath -noout -subject > output.txt

# Here is output which match our configuration(i.e. CN=group-8)
# subject=DC = in, DC = iitb, DC = bhilai, O = IIT Bhilai, CN = group-8