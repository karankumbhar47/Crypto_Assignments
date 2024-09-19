keys=$(openssl rand -hex 12)
echo "k0 = ${keys:0:4}"
echo "k1 = ${keys:4:4}"
echo "k2 = ${keys:8:4}"
echo "k3 = ${keys:12:4}"
echo "k4 = ${keys:16:4}"
echo "k5 = ${keys:20:4}"